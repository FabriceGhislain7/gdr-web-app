from flask import request, render_template, redirect, url_for, flash, session
from . import environment_bp
from gioco.ambiente import AmbienteFactory, Ambiente
from utils.log import Log


@environment_bp.route('/select_environment', methods=['GET', 'POST'])
def select_environment():
    return redirect(url_for('gioco.coming_soon_session'))



@environment_bp.route('/show-environment')
def show_environment():
    return redirect(url_for('gioco.coming_soon_session'))


@staticmethod
def descrizione():
    return redirect(url_for('gioco.coming_soon_session'))
