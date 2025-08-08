import logging
from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from . import inventory_bp

# Import delle classi refactorizzate per inventory
from .utils import (
    InventoryValidator, InventoryManager, InventoryOperations,
    InventoryStatsCalculator, InventoryLogger
)

# Import delle classi refactorizzate per characters
from characters.utils import CharacterManager

from gioco.schemas.inventario import InventarioSchema
from gioco.inventario import Inventario
from marshmallow import ValidationError
import os
from config import DATA_DIR_INV

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Schema initialization
inventario_schema = InventarioSchema()

# ------------------------VISUALIZZA INVENTARIO-----------------------------
@inventory_bp.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    """
    Visualizza inventario del personaggio selezionato con
    caricamento dati da file JSON e validazione.
    """
    # Usa le classi refactorizzate per characters
    owned_ids = CharacterManager.filter_owned_characters(current_user.character_ids or [])
    personaggi = CharacterManager.load_multiple_characters_json(owned_ids)
    nome_per_id = {p['id']: p['nome'] for p in personaggi}

    # Ottieni ID personaggio da GET o POST
    id_personaggio = (
        request.args.get('personaggio_id') if request.method == 'GET'
        else request.form.get('personaggio_id')
    )

    # Trova personaggio selezionato
    personaggio = next((p for p in personaggi if p['id'] == id_personaggio), None)
    inventario_selezionato = None

    if id_personaggio:
        # Carica inventario con le classi refactorizzate
        inventario_selezionato = InventoryManager.load_inventory_json(id_personaggio)

        if inventario_selezionato:
            nome_proprietario = nome_per_id.get(id_personaggio, 'sconosciuto')

            # Log operazione con le classi refactorizzate
            InventoryLogger.log_inventory_operation(
                "viewed", inventario_selezionato, current_user.email,
                proprietario=nome_proprietario
            )

            logger.info(f"Inventario di {nome_proprietario} caricato da JSON.")
        else:
            flash("Inventario non trovato o errore nel file.", "warning")

    return render_template(
        'inventory.html',
        personaggi=personaggi,
        nome_per_id=nome_per_id,
        id_selezionato=id_personaggio if request.method == 'POST' else None,
        id_passato=id_personaggio if request.method == 'GET' else None,
        inventario=inventario_selezionato,
        personaggio=personaggio
    )

# ------------------------AGGIUNGI OGGETTO----------------------------------
@inventory_bp.route('/add_object', methods=['GET', 'POST'])
@login_required
def add_object():
    """
    Aggiunge nuovo oggetto all'inventario del personaggio
    con validazione e salvataggio automatico.
    """
    # Ottieni classi oggetti disponibili con le classi refactorizzate
    oggetti_classes = InventoryValidator.get_object_classes()

    # Ottieni ID personaggio
    personaggio_id = request.args.get('personaggio_id') or request.form.get('personaggio_id')
    if not personaggio_id:
        flash("ID personaggio mancante", "danger")
        return redirect(url_for('inventory.inventory'))

    # Carica e valida personaggio con le classi refactorizzate
    owned_ids = CharacterManager.filter_owned_characters(current_user.character_ids or [])
    personaggi = CharacterManager.load_multiple_characters_json(owned_ids)
    personaggio = next((p for p in personaggi if p['id'] == personaggio_id), None)

    if not personaggio:
        flash("Personaggio non trovato", "danger")
        return redirect(url_for('inventory.inventory'))

    # Carica inventario con le classi refactorizzate
    inventario_pg = InventoryManager.load_inventory_json(personaggio_id)
    if not inventario_pg:
        flash("Inventario non trovato", "danger")
        return redirect(url_for('inventory.inventory'))

    if request.method == 'POST':
        oggetto_sel = request.form.get('oggetto')
        nome_custom = request.form.get('nome_custom', '').strip()
        valore_custom = request.form.get('valore_custom', '0')

        # Validazione oggetto con le classi refactorizzate
        valid_object, object_error = InventoryValidator.validate_object_class(oggetto_sel)
        if not valid_object:
            flash(object_error, "danger")
            return redirect(url_for('inventory.add_object', personaggio_id=personaggio_id))

        try:
            # Validazione valore personalizzato
            try:
                valore_custom = int(valore_custom) if valore_custom else 0
            except ValueError:
                flash("Valore deve essere un numero", "danger")
                return redirect(url_for('inventory.add_object', personaggio_id=personaggio_id))

            # Crea oggetto con le classi refactorizzate
            if nome_custom:
                # Validazione nome personalizzato con le classi refactorizzate
                valid_name, name_error = InventoryValidator.validate_object_name(nome_custom)
                if not valid_name:
                    flash(name_error, "danger")
                    return redirect(url_for('inventory.add_object', personaggio_id=personaggio_id))

                valid_value, value_error = InventoryValidator.validate_object_value(valore_custom)
                if not valid_value:
                    flash(value_error, "danger")
                    return redirect(url_for('inventory.add_object', personaggio_id=personaggio_id))

                nuovo_oggetto = InventoryManager.create_custom_object(oggetto_sel, nome_custom, valore_custom)
            else:
                nuovo_oggetto = InventoryManager.create_object_instance(oggetto_sel)

            # Aggiunge oggetto all'inventario con le classi refactorizzate
            success, message = InventoryOperations.add_object_to_inventory(inventario_pg, nuovo_oggetto)

            if success:
                # Log operazione con le classi refactorizzate
                InventoryLogger.log_inventory_operation(
                    "object_added", inventario_pg, current_user.email,
                    oggetto_nome=nuovo_oggetto.nome, oggetto_tipo=oggetto_sel
                )

                flash(f"Oggetto '{nuovo_oggetto.nome}' aggiunto a {personaggio['nome']}", "success")
                return redirect(url_for('inventory.inventory', personaggio_id=personaggio_id))
            else:
                flash(message, "danger")

        except Exception as e:
            logger.error(f"Errore aggiunta oggetto: {str(e)}")
            flash("Errore durante l'aggiunta dell'oggetto", "danger")

    return render_template(
        'edit_object.html',
        oggetti=list(oggetti_classes.keys()),
        personaggio=personaggio,
        personaggio_id=personaggio_id
    )

# ------------------------ELIMINA OGGETTO-----------------------------------
@inventory_bp.route('/delete-object/<string:oggetto_id>', methods=['POST'])
@login_required
def delete_object(oggetto_id):
    """
    Elimina oggetto dall'inventario con validazione ownership
    e aggiornamento automatico file JSON.
    """
    # Recupera ID personaggio dal form
    personaggio_id = request.form.get('personaggio_id')
    if not personaggio_id:
        flash("ID personaggio mancante", "danger")
        return redirect(url_for('inventory.inventory'))

    # Validazione ownership personaggio con le classi refactorizzate
    owned_ids = CharacterManager.filter_owned_characters(current_user.character_ids or [])
    personaggi = CharacterManager.load_multiple_characters_json(owned_ids)

    personaggio = next((p for p in personaggi if p['id'] == personaggio_id), None)
    if not personaggio:
        flash("Personaggio non trovato", "danger")
        return redirect(url_for('inventory.inventory'))

    # Carica inventario con le classi refactorizzate
    inventario_pg = InventoryManager.load_inventory_json(personaggio_id)
    if not inventario_pg:
        flash("Inventario non trovato", "danger")
        return redirect(url_for('inventory.inventory'))

    try:
        # Rimuove oggetto con le classi refactorizzate
        success, message, oggetto_rimosso = InventoryOperations.remove_object_from_inventory(inventario_pg, oggetto_id)

        if success and oggetto_rimosso:
            # Log operazione con le classi refactorizzate
            InventoryLogger.log_inventory_operation(
                "object_removed", inventario_pg, current_user.email,
                oggetto_id=oggetto_id, oggetto_nome=oggetto_rimosso.nome
            )

            flash(f"Oggetto '{oggetto_rimosso.nome}' rimosso da {personaggio['nome']}", "success")
        else:
            flash(message, "warning")

    except Exception as e:
        logger.error(f"Errore eliminazione oggetto {oggetto_id}: {str(e)}")
        flash("Errore durante l'eliminazione dell'oggetto", "danger")

    return redirect(url_for('inventory.inventory', personaggio_id=personaggio_id))

# ------------------------USA OGGETTO---------------------------------------
@inventory_bp.route('/use_object', methods=['POST'])
@login_required
def use_object():
    """
    Utilizza oggetto dall'inventario su un bersaglio specificato
    con gestione effetti e aggiornamento stato.
    """
    try:
        # Raccolta dati dal form
        personaggio_id = request.form.get('personaggio_id')
        oggetto_nome = request.form.get('oggetto_nome')
        bersaglio_id = request.form.get('bersaglio_id')

        if not all([personaggio_id, oggetto_nome, bersaglio_id]):
            flash("Dati mancanti per l'utilizzo dell'oggetto", "danger")
            return redirect(url_for('inventory.inventory'))

        # Carica personaggi e inventario con le classi refactorizzate
        owned_ids = CharacterManager.filter_owned_characters(current_user.character_ids or [])
        personaggi = CharacterManager.load_multiple_characters_json(owned_ids)

        # Trova utilizzatore e bersaglio
        utilizzatore = next((p for p in personaggi if p['id'] == personaggio_id), None)
        bersaglio = next((p for p in personaggi if p['id'] == bersaglio_id), None)

        if not utilizzatore or not bersaglio:
            flash("Personaggio utilizzatore o bersaglio non trovato", "danger")
            return redirect(url_for('inventory.inventory', personaggio_id=personaggio_id))

        # Carica inventario con le classi refactorizzate
        inventario_pg = InventoryManager.load_inventory_json(personaggio_id)
        if not inventario_pg:
            flash("Inventario non trovato", "danger")
            return redirect(url_for('inventory.inventory', personaggio_id=personaggio_id))

        # Usa oggetto con le classi refactorizzate
        success, message = InventoryOperations.use_object_in_inventory(
            inventario_pg, oggetto_nome, utilizzatore, bersaglio
        )

        if success:
            # Log operazione con le classi refactorizzate
            InventoryLogger.log_inventory_operation(
                "object_used", inventario_pg, current_user.email,
                oggetto_nome=oggetto_nome, 
                utilizzatore=utilizzatore['nome'],
                bersaglio=bersaglio['nome']
            )

            flash(f"Oggetto '{oggetto_nome}' utilizzato con successo", "success")
        else:
            flash(message, "danger")

    except Exception as e:
        logger.error(f"Errore utilizzo oggetto: {str(e)}")
        flash("Errore durante l'utilizzo dell'oggetto", "danger")

    return redirect(url_for('inventory.inventory', personaggio_id=personaggio_id))

# ------------------------STATISTICHE INVENTARIO----------------------------
@inventory_bp.route('/inventory_stats/<string:personaggio_id>')
@login_required
def inventory_stats(personaggio_id):
    """
    Mostra statistiche dettagliate dell'inventario del personaggio
    con analisi valore, tipologie e distribuzioni.
    """
    try:
        # Validazione ownership con le classi refactorizzate
        owned_ids = CharacterManager.filter_owned_characters(current_user.character_ids or [])
        personaggi = CharacterManager.load_multiple_characters_json(owned_ids)

        personaggio = next((p for p in personaggi if p['id'] == personaggio_id), None)
        if not personaggio:
            flash("Personaggio non trovato", "danger")
            return redirect(url_for('inventory.inventory'))

        # Carica inventario con le classi refactorizzate
        inventario_pg = InventoryManager.load_inventory_json(personaggio_id)
        if not inventario_pg:
            flash("Inventario non trovato", "danger")
            return redirect(url_for('inventory.inventory'))

        # Ottieni statistiche con le classi refactorizzate
        item_count = InventoryStatsCalculator.get_inventory_item_count(inventario_pg)
        total_value = InventoryStatsCalculator.get_inventory_value_total(inventario_pg)
        stats_by_type = InventoryStatsCalculator.get_inventory_stats_by_type(inventario_pg)
        debug_info = InventoryLogger.get_inventory_debug_info(inventario_pg)

        # Log visualizzazione statistiche con le classi refactorizzate
        InventoryLogger.log_inventory_operation(
            "stats_viewed", inventario_pg, current_user.email,
            personaggio_nome=personaggio['nome']
        )

        return render_template(
            'inventory_stats.html',
            personaggio=personaggio,
            item_count=item_count,
            total_value=total_value,
            stats_by_type=stats_by_type,
            debug_info=debug_info
        )

    except Exception as e:
        logger.error(f"Errore caricamento statistiche inventario {personaggio_id}: {str(e)}")
        flash("Errore caricamento statistiche", "danger")
        return redirect(url_for('inventory.inventory'))

# ------------------------API INVENTARIO------------------------------------
@inventory_bp.route('/api/inventory/<string:personaggio_id>')
@login_required
def inventory_api(personaggio_id):
    """
    API endpoint per dati inventario in formato JSON
    per dashboard dinamiche e AJAX calls.
    """
    try:
        # Validazione ownership con le classi refactorizzate
        owned_ids = CharacterManager.filter_owned_characters(current_user.character_ids or [])

        if personaggio_id not in owned_ids:
            return jsonify({'success': False, 'error': 'Personaggio non autorizzato'}), 403

        # Carica inventario con le classi refactorizzate
        inventario_pg = InventoryManager.load_inventory_json(personaggio_id)
        if not inventario_pg:
            return jsonify({'success': False, 'error': 'Inventario non trovato'}), 404

        # Prepara dati per API con le classi refactorizzate
        stats = {
            'item_count': InventoryStatsCalculator.get_inventory_item_count(inventario_pg),
            'total_value': InventoryStatsCalculator.get_inventory_value_total(inventario_pg),
            'stats_by_type': InventoryStatsCalculator.get_inventory_stats_by_type(inventario_pg),
            'oggetti': inventario_pg.get('oggetti', [])
        }

        return jsonify({
            'success': True,
            'personaggio_id': personaggio_id,
            'stats': stats
        })

    except Exception as e:
        logger.error(f"Errore API inventario {personaggio_id}: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ------------------------RICERCA OGGETTI-----------------------------------
@inventory_bp.route('/search_objects/<string:personaggio_id>')
@login_required
def search_objects(personaggio_id):
    """
    Ricerca oggetti nell'inventario con criteri multipli.
    """
    try:
        # Validazione ownership con le classi refactorizzate
        owned_ids = CharacterManager.filter_owned_characters(current_user.character_ids or [])
        personaggi = CharacterManager.load_multiple_characters_json(owned_ids)

        personaggio = next((p for p in personaggi if p['id'] == personaggio_id), None)
        if not personaggio:
            flash("Personaggio non trovato", "danger")
            return redirect(url_for('inventory.inventory'))

        # Carica inventario con le classi refactorizzate
        inventario_pg = InventoryManager.load_inventory_json(personaggio_id)
        if not inventario_pg:
            flash("Inventario non trovato", "danger")
            return redirect(url_for('inventory.inventory'))

        # Ottieni criteri di ricerca dai parametri query
        criteria = {}
        if request.args.get('nome'):
            criteria['nome'] = request.args.get('nome')
        if request.args.get('tipo'):
            criteria['tipo'] = request.args.get('tipo')
        if request.args.get('valore_min'):
            criteria['valore_min'] = int(request.args.get('valore_min'))
        if request.args.get('valore_max'):
            criteria['valore_max'] = int(request.args.get('valore_max'))

        # Esegui ricerca con le classi refactorizzate
        risultati = InventoryOperations.find_objects_in_inventory(inventario_pg, criteria)

        # Log operazione ricerca con le classi refactorizzate
        InventoryLogger.log_inventory_operation(
            "search_performed", inventario_pg, current_user.email,
            criteria=str(criteria), risultati_count=len(risultati)
        )

        return render_template(
            'inventory_search.html',
            personaggio=personaggio,
            criteri=criteria,
            risultati=risultati,
            inventario=inventario_pg
        )

    except Exception as e:
        logger.error(f"Errore ricerca oggetti inventario {personaggio_id}: {str(e)}")
        flash("Errore durante la ricerca", "danger")
        return redirect(url_for('inventory.inventory', personaggio_id=personaggio_id))

# ------------------------COMPATIBILITÀ CON CODICE ESISTENTE---------------
def salva_inventario_su_json(inventario: Inventario):
    """
    Funzione di compatibilità per il codice esistente.
    Mantiene l'interfaccia originale ma usa le classi refactorizzate.
    
    Args:
        inventario (Inventario): Istanza inventario da salvare
    """
    try:
        success = InventoryManager.save_inventory_json(inventario)
        if success:
            logger.info("Inventario salvato tramite funzione compatibilità")
        else:
            logger.error("Errore salvataggio inventario tramite funzione compatibilità")
    except Exception as e:
        logger.error(f"Errore funzione compatibilità salvataggio: {str(e)}")
        raise

def carica_inventario_da_json(personaggio_id: str):
    """
    Funzione di compatibilità per il codice esistente.
    Mantiene l'interfaccia originale ma usa le classi refactorizzate.
    
    Args:
        personaggio_id (str): ID del personaggio proprietario
        
    Returns:
        Dict o None: Dati inventario o None se non trovato
    """
    try:
        return InventoryManager.load_inventory_json(personaggio_id)
    except Exception as e:
        logger.error(f"Errore funzione compatibilità caricamento: {str(e)}")
        return None