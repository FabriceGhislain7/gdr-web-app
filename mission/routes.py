import json
import os
from collections import defaultdict

from flask import flash, render_template, request, session, redirect, url_for
from flask_login import login_required

from . import mission_bp
from config import DATA_DIR_MIS
from gioco.ambiente import AmbienteFactory
from gioco.schemas.missione import MissioniSchema
from gioco.missione import Missione


def _load_missions():
    schema = MissioniSchema()
    missioni = []
    for file_name in os.listdir(DATA_DIR_MIS):
        if not file_name.endswith(".json"):
            continue
        path = os.path.join(DATA_DIR_MIS, file_name)
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        missioni.append(schema.load(data))
    return missioni


def _get_selected_environment():
    env_data = session.get("ambiente")
    if not env_data:
        return None
    scelta = str(env_data.get("classe", "1"))
    mapping = AmbienteFactory.get_opzioni()
    if scelta in mapping:
        return AmbienteFactory.usa_ambiente(scelta)

    scelta_lower = scelta.lower()
    for key, ambiente in mapping.items():
        if ambiente.__class__.__name__.lower() == scelta_lower or ambiente.nome.lower() == scelta_lower:
            return AmbienteFactory.usa_ambiente(key)
    return AmbienteFactory.usa_ambiente("1")


@mission_bp.route('/select_mission', methods=['GET', 'POST'])
@login_required
def select_mission():
    missioni = _load_missions()
    if not missioni:
        flash("Nessuna missione disponibile. Controlla i file JSON missione.", "danger")
        return redirect(url_for("gioco.menu"))

    if request.method == 'POST':
        missione_id = request.form.get('missione_id')
        missione_selezionata = next(
            (m for m in missioni if str(m.id) == str(missione_id)),
            None
        )

        if not missione_selezionata:
            flash("Missione non trovata.", "danger")
            return redirect(url_for("mission.select_mission"))

        ambiente_selezionato = _get_selected_environment()
        if ambiente_selezionato:
            missione_selezionata.ambiente = ambiente_selezionato

        session["missione"] = MissioniSchema().dump(missione_selezionata)
        flash(f"Missione selezionata: {missione_selezionata.nome}", "success")
        return redirect(url_for('mission.show_mission'))

    return render_template('select_mission.html', missioni=missioni)


@mission_bp.route('/show_mission')
@login_required
def show_mission():
    missione_data = session.get("missione")
    if not missione_data:
        flash("Nessuna missione selezionata.", "warning")
        return redirect(url_for('mission.select_mission'))

    missione = MissioniSchema().load(missione_data)
    premi_raggruppati = defaultdict(list)
    for premio in missione.premi:
        premi_raggruppati[premio.nome].append(premio)

    return render_template(
        'show_mission.html',
        missione=missione,
        ambiente=missione.ambiente,
        premi_raggruppati=premi_raggruppati
    )


@mission_bp.route('/missioni')
@login_required
def mostra_missioni():
    return redirect(url_for('mission.select_mission'))


@mission_bp.route('/missione/attiva')
@login_required
def missione_attiva():
    return redirect(url_for('mission.show_mission'))


@mission_bp.route('/missioni/stato')
@login_required
def stato_missioni():
    missione_data = session.get("missione")
    if not missione_data:
        flash("Nessuna missione attiva.", "warning")
        return redirect(url_for('mission.select_mission'))
    missione = MissioniSchema().load(missione_data)
    stato = "completata" if missione.completata else "in corso"
    flash(f"Missione '{missione.nome}': {stato}.", "info")
    return redirect(url_for('mission.show_mission'))
