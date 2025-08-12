from flask import Blueprint, render_template, request, session, redirect, url_for
from gioco.personaggio import Personaggio
from gioco.classi import Mago, Guerriero, Ladro
from flask_login import login_user, logout_user, login_required, current_user, UserMixin 
from characters.utils import CharacterStatsCalculator
import os

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
gioco_bp = Blueprint('gioco', __name__, template_folder=template_dir)

# ----------------------HOME_PAGE------------------------------------
@gioco_bp.route('/')
def index():
    return render_template('index.html')

#-----------------------ABOUT---------------------------------------
@gioco_bp.route('/about')
def about():
    return render_template('about.html')

#-----------------------GUIDE_GAME----------------------------------
@gioco_bp.route('/guide_game')
def guide_game():
    return render_template('guide_game.html')

#-----------------------CREDITS--------------------------------------
@gioco_bp.route("/credits")
def credits():
    return render_template("credits.html")

#-----------------------MENU_PRINCIPALE------------------------------
@gioco_bp.route('/menu')
@login_required
def menu():
    owner_char = current_user.character_ids
    stat_char = CharacterStatsCalculator.get_user_character_stats_by_class(owner_char)
    print(f"STAT_CHARS =================================>   {stat_char}")
    num_guerrieri = stat_char["Guerriero"]
    num_maghi = stat_char["Mago"]
    num_ladri = stat_char["Ladro"]

    return render_template('menu.html',
                           num_guerrieri=num_guerrieri,
                           num_ladri=num_ladri,
                           num_maghi=num_maghi)

# -----------------------CLEAR THE SESION ---------------------------
@gioco_bp.route('/clear')
def clear():
    session.clear()
    return redirect(url_for('gioco.index'))

# ----------------------- COMING-SOON PAGE ---------------------------
@gioco_bp.route('/coming_soon')
def coming_soon_session():
    # Questo temlpate serve per non creare errori per le funzionalità ancora in svillupo.
    return render_template('coming_soon.html')