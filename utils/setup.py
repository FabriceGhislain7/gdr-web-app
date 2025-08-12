from werkzeug.security import generate_password_hash
from auth.models import User, UserRole
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_administrator():
    admin = User(nome = "Admin",
                 email = "admin@admin.it",
                 password_hash = generate_password_hash("1234"),
                 crediti=10000000,
                 character_ids=[],
                 ruolo=UserRole.ADMIN
                 )
    return admin

def create_player():
    player = User(nome = "Player",
                  email = "player@player.com",
                  password_hash = generate_password_hash("Player@7"),
                  crediti = 1000000,
                  character_ids=[],
                  ruolo=UserRole.PLAYER
                  )
    return player

def create_developer():
    player = User(nome = "Developer",
                  email = "developer@developer.com",
                  password_hash = generate_password_hash("Developer@7"),
                  crediti = 1000000,
                  character_ids=[],
                  ruolo=UserRole.TEAM_MEMBER_DEVELOPER
                  )
    return player