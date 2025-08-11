import os
import json
import logging
from flask import render_template, request, redirect, url_for, session, abort, flash, jsonify
from flask_login import login_required, current_user
from inventory.utils import InventoryValidator, InventoryManager
from gioco.schemas.personaggio import PersonaggioSchema
from auth.models import db
from config import CreateDirs
from . import characters_bp
from .utils import (CharacterValidator, CharacterManager, CharacterStatsCalculator,
                    CharacterCombat, CharacterLogger)

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Schema initialization
schema = PersonaggioSchema()

# ------------------------CARICA PERSONAGGI POSSEDUTI----------------------
@characters_bp.route('/load_char')
@login_required
def load_char():
    """
    Carica IDs dei personaggi posseduti dall'utente confrontando
    file JSON esistenti con character_ids nel database.
    """
    # Ottieni tutti i file JSON dei personaggi
    all_char_files = CharacterManager.get_user_character_files()
    
    # Filtra solo quelli posseduti dall'utente
    owned_chars = CharacterManager.filter_owned_characters(current_user.character_ids or [])
    
    # Gestione caso utente senza personaggi
    if not owned_chars:
        return []

    logger.info(f"Caricati {len(owned_chars)} personaggi per utente {current_user.email}")
    return owned_chars

# ------------------------CREA PERSONAGGIO----------------------------------
@characters_bp.route('/create_char', methods=['GET', 'POST'])
@login_required
def create_char():
    """
    Gestisce creazione nuovo personaggio con validazione crediti,
    salvataggio file JSON e creazione inventario iniziale.
    """
    CreateDirs()  # Verifica esistenza cartelle
    
    from app import db
    
    # Ottieni mapping classi e oggetti disponibili
    classi = CharacterValidator.get_character_classes()
    oggetti = InventoryValidator.get_object_classes()

    if request.method == 'POST':
        # Raccolta dati dal form
        nome = request.form['nome'].strip()
        classe_sel = request.form['classe']
        oggetto_sel = request.form['oggetto']

        # Validazione input con le classi refactorizzate
        valid_name, name_error = CharacterValidator.validate_character_name(nome)
        if not valid_name:
            flash(name_error, "danger")
            return redirect(url_for('characters.create_char'))

        valid_class, class_error = CharacterValidator.validate_character_class(classe_sel)
        if not valid_class:
            flash(class_error, "danger")
            return redirect(url_for('characters.create_char'))

        valid_object, object_error = InventoryValidator.validate_object_class(oggetto_sel)
        if not valid_object:
            flash(object_error, "danger")
            return redirect(url_for('characters.create_char'))

        try:
            # Creazione personaggio e oggetto iniziale con le classi refactorizzate
            pg = CharacterManager.create_character_instance(nome, classe_sel)
            ogg = InventoryManager.create_object_instance(oggetto_sel)
            inv = InventoryManager.create_character_inventory(str(pg.id), ogg)

            # Controllo crediti disponibili
            costo_pg = CharacterStatsCalculator.calculate_character_cost(pg)
            can_afford, credit_error = CharacterValidator.validate_user_can_afford(current_user.crediti, costo_pg)

            if not can_afford:
                flash(credit_error, "danger")
                return redirect(url_for('auth.personal_area'))

            # Deduzione crediti
            current_user.crediti -= costo_pg

            # Serializzazione e salvataggio con le classi refactorizzate
            pg_dict = schema.dump(pg)
            if not CharacterManager.save_character_json(pg_dict):
                raise Exception("Errore salvataggio personaggio")

            InventoryManager.save_inventory_json(inv)

            # Aggiornamento character_ids utente con le classi refactorizzate
            current_user.character_ids = CharacterManager.update_user_character_ids(
                current_user.character_ids, str(pg.id), 'add'
            )

            db.session.commit()

            # Logging con le classi refactorizzate
            CharacterLogger.log_character_operation(
                "created", pg_dict, current_user.email,
                costo=costo_pg, oggetto_iniziale=oggetto_sel
            )
            
            flash(f"Personaggio {pg.nome} creato! Spesi {costo_pg} crediti.", "success")
            return redirect(url_for('characters.show_chars'))

        except Exception as e:
            db.session.rollback()
            logger.error(f"Errore creazione personaggio: {str(e)}")
            flash("Errore durante la creazione", "danger")

    return render_template(
        'create_char.html',
        classi=classi,
        oggetti=oggetti
    )

# ------------------------MODIFICA PERSONAGGIO------------------------------
@characters_bp.route('/edit_char/<uuid:char_id>', methods=['GET', 'POST'])
@login_required
def edit_char(char_id):
    """
    Modifica personaggio esistente con validazione ownership
    e aggiornamento completo dei dati.
    """
    # Verifica ownership del personaggio
    owned_ids = load_char()
    if str(char_id) not in owned_ids:
        flash("Personaggio non trovato", "danger")
        return redirect(url_for("characters.show_chars"))

    # Caricamento personaggio con le classi refactorizzate
    pg_dict = CharacterManager.load_character_json(str(char_id))
    if not pg_dict:
        flash("Errore caricamento personaggio", "danger")
        return redirect(url_for('characters.show_chars'))

    # Ottieni classi disponibili
    classi = CharacterValidator.get_character_classes()

    if request.method == 'POST':
        try:
            # Raccolta dati modifiche
            vecchio_nome = pg_dict['nome']
            nuovo_nome = request.form['nome'].strip()
            nuova_classe = request.form['classe']

            # Validazione input con le classi refactorizzate
            valid_name, name_error = CharacterValidator.validate_character_name(nuovo_nome)
            if not valid_name:
                flash(name_error, "danger")
                return render_template('char_edit.html', pg=pg_dict, classi=list(classi.keys()))

            valid_class, class_error = CharacterValidator.validate_character_class(nuova_classe)
            if not valid_class:
                flash(class_error, "danger")
                return render_template('char_edit.html', pg=pg_dict, classi=list(classi.keys()))

            # Creazione nuovo oggetto personaggio con le classi refactorizzate
            pg_obj = CharacterManager.create_character_instance(nuovo_nome, nuova_classe)
            # Mantieni ID originale
            pg_obj.id = pg_dict['id']

            # Serializzazione e salvataggio con le classi refactorizzate
            updated_dict = schema.dump(pg_obj)
            if not CharacterManager.save_character_json(updated_dict):
                raise Exception("Errore salvataggio modifiche")

            # Logging con le classi refactorizzate
            CharacterLogger.log_character_operation(
                "updated", updated_dict, current_user.email,
                vecchio_nome=vecchio_nome, nuova_classe=nuova_classe
            )

            flash("Personaggio aggiornato con successo", "success")
            return redirect(url_for('characters.show_chars'))

        except Exception as e:
            logger.error(f"Errore modifica personaggio {char_id}: {str(e)}")
            flash("Errore durante la modifica", "danger")

    return render_template(
        'char_edit.html',
        pg=pg_dict,
        classi=list(classi.keys())
    )

# ------------------------RECUPERA PERSONAGGI POSSEDUTI--------------------
@characters_bp.route('/get_owned_chars')
def get_owned_chars(owned_chars):
    """
    Carica e deserializza personaggi posseduti dall'utente
    usando le classi refactorizzate per gestione JSON.
    """
    # Usa le classi refactorizzate per caricamento multiplo
    personaggi_posseduti = CharacterManager.load_multiple_characters_json(owned_chars)
    return personaggi_posseduti

# ------------------------MOSTRA LISTA PERSONAGGI--------------------------
@characters_bp.route('/characters', methods=['GET'])
@login_required
def show_chars():
    """
    Visualizza lista completa dei personaggi dell'utente
    con caricamento e validazione dati.
    """
    owned_chars = load_char()
    lista_pers_utente = get_owned_chars(owned_chars)
    
    logger.info(f"Lista personaggi richiesta - Count: {len(lista_pers_utente)}")
    
    return render_template(
        'list_char.html',
        personaggi=lista_pers_utente
    )

# ------------------------DETTAGLI PERSONAGGIO------------------------------
@characters_bp.route('/characters/<uuid:char_id>', methods=['GET'])
@login_required
def char_details(char_id):
    """
    Mostra dettagli completi di un personaggio specifico
    con validazione ownership e caricamento sicuro.
    """
    try:
        # Caricamento personaggi posseduti con le classi refactorizzate
        owned_chars = load_char()
        lista_pers = CharacterManager.load_multiple_characters_json(owned_chars)
        
    except Exception as e:
        logger.error(f"Errore caricamento lista personaggi: {str(e)}")
        lista_pers = []

    # Ricerca personaggio per ID con le classi refactorizzate
    pg_dict = CharacterManager.find_character_by_id(lista_pers, str(char_id))

    if pg_dict is None:
        logger.warning(f"Accesso a personaggio inesistente - ID: {char_id}")
        abort(404)

    logger.info(f"Dettagli personaggio visualizzati - ID: {char_id}, Nome: {pg_dict.get('nome', 'N/A')}")
    
    return render_template(
        'char_details.html',
        pg=pg_dict,
        id=char_id
    )

# ------------------------ELIMINA PERSONAGGIO-------------------------------
@characters_bp.route('/characters/<uuid:char_id>', methods=['POST'])
@login_required
def char_delete(char_id):
    """
    Elimina personaggio con rimozione file, inventario
    e rimborso crediti automatico.
    """
    try:
        # Caricamento dati personaggio con le classi refactorizzate
        pg_dict = CharacterManager.load_character_json(str(char_id))
        if not pg_dict:
            flash("File personaggio non raggiungibile", "danger")
            return redirect(url_for('characters.show_chars'))

        # Deserializzazione per rimborso crediti
        pg_obj = schema.load(pg_dict)

        # Eliminazione file personaggio e inventario con le classi refactorizzate
        if not CharacterManager.delete_character_json(str(char_id)):
            logger.warning(f"Problemi eliminazione file personaggio {char_id}")

        if not InventoryManager.delete_inventory_json(str(char_id)):
            logger.warning(f"Problemi eliminazione inventario {char_id}")

        # Rimozione UUID dalla lista utente con le classi refactorizzate
        current_user.character_ids = CharacterManager.update_user_character_ids(
            current_user.character_ids, str(char_id), 'remove'
        )

        # Rimborso crediti con le classi refactorizzate
        rimborso = CharacterStatsCalculator.calculate_character_refund(pg_obj)
        current_user.crediti += rimborso

        db.session.commit()
        
        # Logging con le classi refactorizzate
        CharacterLogger.log_character_operation(
            "deleted", pg_dict, current_user.email,
            rimborso=rimborso
        )
        
        flash(f"Personaggio eliminato! Rimborsati {rimborso} crediti.", "success")

    except Exception as e:
        db.session.rollback()
        logger.error(f"Errore eliminazione personaggio {char_id}: {str(e)}")
        flash("Errore durante l'eliminazione", "danger")

    return redirect(url_for('characters.show_chars'))

# ------------------------COMBATTIMENTO-------------------------------------
@characters_bp.route('/combattimento', methods=['GET', 'POST'])
@login_required
def begin_combat():
    """
    Sistema di combattimento tra personaggi dell'utente
    con simulazione turni e meccaniche di successo/fallimento.
    """
    # Filtro personaggi dell'utente dalla sessione
    lista_pers = session.get('personaggi', [])
    personaggi_utente = [p for p in lista_pers if p['id'] in (current_user.character_ids or [])]

    if request.method == 'POST':
        try:
            # Raccolta IDs combattenti
            id_1 = request.form['pg1']
            id_2 = request.form['pg2']

            # Ricerca personaggi con le classi refactorizzate
            pg1_dict = CharacterManager.find_character_by_id(personaggi_utente, id_1)
            pg2_dict = CharacterManager.find_character_by_id(personaggi_utente, id_2)

            if not pg1_dict or not pg2_dict:
                abort(400, "Personaggio non trovato.")

            # Deserializzazione personaggi
            pg1 = schema.load(pg1_dict)
            pg2 = schema.load(pg2_dict)

            # Inizializzazione combattimento
            log_combattimento = []
            turno = 1

            # Loop combattimento con meccaniche avanzate usando le classi refactorizzate
            while pg1.salute > 0 and pg2.salute > 0:
                log_combattimento.append(f"Turno {turno}:")

                # Turno personaggio 1 con le classi refactorizzate
                successo, danno, messaggio = CharacterCombat.execute_combat_turn(pg1, pg2)
                log_combattimento.append(messaggio)

                if pg2.salute <= 0:
                    break

                # Turno personaggio 2 con le classi refactorizzate
                successo, danno, messaggio = CharacterCombat.execute_combat_turn(pg2, pg1)
                log_combattimento.append(messaggio)

                turno += 1

            # Determinazione vincitore con le classi refactorizzate
            risultato = CharacterCombat.determine_combat_winner(pg1, pg2)
            log_combattimento.append(f"Risultato finale: {risultato}")
            
            logger.info(f"Combattimento completato - {risultato}")

            return render_template(
                'combat.html',
                pg1=pg1,
                pg2=pg2,
                risultato=risultato,
                log_combattimento=log_combattimento
            )

        except Exception as e:
            logger.error(f"Errore durante combattimento: {str(e)}")
            flash("Errore durante il combattimento", "danger")

    return render_template('combat.html', personaggi=personaggi_utente)

# ------------------------DASHBOARD STATISTICHE-----------------------------
@characters_bp.route('/dashboard')
@login_required
def character_dashboard():
    """
    Dashboard con statistiche dettagliate sui personaggi dell'utente.
    """
    try:
        # Ottieni tutte le statistiche con le classi refactorizzate
        total_count = CharacterStatsCalculator.get_user_character_count(current_user.character_ids or [])
        stats_by_class = CharacterStatsCalculator.get_user_character_stats_by_class(current_user.character_ids or [])
        most_played, most_count = CharacterStatsCalculator.get_most_played_class(current_user.character_ids or [])
        
        return render_template(
            'character_dashboard.html',
            total_count=total_count,
            stats=stats_by_class,
            most_played=most_played,
            most_count=most_count
        )
        
    except Exception as e:
        logger.error(f"Errore caricamento dashboard: {str(e)}")
        flash("Errore caricamento statistiche", "warning")
        return redirect(url_for('characters.show_chars'))

# ------------------------API STATISTICHE-----------------------------------
@characters_bp.route('/api/stats')
@login_required
def character_stats_api():
    """
    API endpoint per statistiche personaggi (per AJAX/dashboard dinamica).
    """
    try:
        stats = CharacterStatsCalculator.get_user_character_stats_by_class(current_user.character_ids or [])
        return jsonify({
            'success': True,
            'stats': stats,
            'total': stats.get('Totale', 0)
        })
    except Exception as e:
        logger.error(f"Errore API statistiche: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500