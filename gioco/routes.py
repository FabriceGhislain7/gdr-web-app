from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user
from characters.utils import CharacterStatsCalculator
import os
from utils.i18n import get_current_language, set_current_language, translate

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
gioco_bp = Blueprint('gioco', __name__, template_folder=template_dir)


@gioco_bp.app_context_processor
def inject_i18n_helpers():
    return {
        "t": translate,
        "current_language": get_current_language()
    }


@gioco_bp.route('/set-language/<lang>')
def set_language(lang):
    set_current_language(lang)
    next_url = request.args.get("next", "").strip()
    if not next_url.startswith("/"):
        next_url = url_for("gioco.index")
    return redirect(next_url)

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
