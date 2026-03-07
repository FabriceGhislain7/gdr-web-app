from flask import render_template, redirect, request, session, url_for, flash
from flask_login import login_required

from . import environment_bp
from gioco.ambiente import AmbienteFactory


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


@environment_bp.route('/select_environment', methods=['GET', 'POST'])
@login_required
def select_environment():
    opzioni = AmbienteFactory.get_opzioni()

    if request.method == 'POST':
        scelta = request.form.get('ambiente')
        if not scelta:
            flash("Seleziona un ambiente.", "warning")
            return redirect(url_for('environment.select_environment'))

        ambiente = AmbienteFactory.usa_ambiente(scelta)
        session["ambiente"] = ambiente.to_dict()
        flash(f"Ambiente selezionato: {ambiente.nome}", "success")
        return redirect(url_for('environment.show_environment'))

    ambiente_corrente = _get_selected_environment()
    return render_template(
        'select_environment.html',
        opzioni=opzioni,
        ambiente_corrente=ambiente_corrente
    )


@environment_bp.route('/show-environment')
@login_required
def show_environment():
    ambiente = _get_selected_environment()
    if not ambiente:
        flash("Nessun ambiente selezionato.", "warning")
        return redirect(url_for('environment.select_environment'))

    return render_template('show_environment.html', ambiente=ambiente)
