import os
from flask import Flask
from flask_session import Session
from battle.routes import battle_bp
from characters.routes import characters_bp
from environment.routes import environment_bp
from inventory.routes import inventory_bp
from mission.routes import mission_bp
from statistics.routes import statistics_bp
from auth.routes import auth_bp
from flask_migrate import Migrate
from auth.models import db, User
from flask_login import LoginManager
from config import CreateDirs, create_leaderboard
from utils.setup import create_player, create_administrator, create_developer
from datetime import timedelta
from gioco.routes import gioco_bp

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    CreateDirs()  # crea directory necessarie per i file JSON
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cambia_questa_chiave_per_una_più_sicura')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'      # Configurazione per il database.
    db.init_app(app)
    migrate = Migrate(app, db)  # Assegnata non utilizzata
    login_manager.init_app(app)
    Session(app)
    app.permanent_session_lifetime = timedelta(minutes=30)     # imposta la durata della sessione a 30 minuti

    app.register_blueprint(gioco_bp)
    app.register_blueprint(battle_bp)
    app.register_blueprint(characters_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(mission_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(statistics_bp)
    app.register_blueprint(environment_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        create_leaderboard()  # aggiorna classifica all'avvio

        # Aggiungo un utente Admin al DB se già non esiste
        if not User.query.filter_by(email="admin@admin.it").first():
            admin = create_administrator()
            db.session.add(admin)
            db.session.commit()

        #  Aggiunta di un utente Player per visualizzare
        if not User.query.filter_by(email="player@player.com").first():
            player = create_player()
            db.session.add(player)
            db.session.commit()

        #  Aggiunta di un utente Player per visualizzare
        if not User.query.filter_by(email="developer@developer.com").first():
            player = create_developer()
            db.session.add(player)
            db.session.commit()

    app.run(debug=True, host="0.0.0.0", port=5001)