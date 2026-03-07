# Integrazione SQLAlchemy in progetto Flask GDR – Versione 1.0

Questa guida documenta l'integrazione del sistema di **autenticazione utenti**, **gestione personaggi** e **salvataggio su database SQLAlchemy** in un'app Flask per gioco di ruolo (GDR).

---

# Obiettivo della v1.0

Un'applicazione web con:

* Registrazione utenti
* Login / Logout
* Creazione personaggi associati all’utente
* Persistenza su database SQLite
* Flask + SQLAlchemy

---

# Struttura consigliata del progetto

```bash
gdr-web-app/
│
├── app.py
├── config.py
│
├── /templates
│   ├── layout.html
│   ├── login.html
│   ├── signup.html
│   └── dashboard.html
│
├── /auth
│   └── routes.py
│
├── /characters
│   └── routes.py
│
├── /database
│   ├── db.py
│   ├── models.py
│   └── seed.py
│
├── /utils
│   └── salvataggio.py
```

---

# Dipendenze richieste

```
pip install Flask Flask-SQLAlchemy Flask-Session Werkzeug
```

---

# Database initialization

## database/db.py

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

---

# Modelli database

## database/models.py

```python
from .db import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    personaggi = db.relationship(
        'Personaggio',
        backref='utente',
        lazy=True,
        cascade="all, delete"
    )


class Personaggio(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(50), nullable=False)

    classe = db.Column(db.String(50), nullable=False)

    salute = db.Column(db.Integer, default=100)

    attacco_min = db.Column(db.Integer, default=5)

    attacco_max = db.Column(db.Integer, default=15)

    livello = db.Column(db.Integer, default=1)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
```

---

# Configurazione Flask

## app.py

```python
from flask import Flask
from flask_session import Session

from database.db import db

from auth.routes import auth_bp
from characters.routes import characters_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'cambia_questa_chiave'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gdr.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    db.init_app(app)
    Session(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(characters_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()

    app.run(debug=True)
```

---

# Sistema di autenticazione

## auth/routes.py

```python
from flask import Blueprint, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db
from database.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "Username già esistente"

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))

    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect("/dashboard")

        return "Credenziali non valide"
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
```

---

# Gestione personaggi

## characters/routes.py

```python
from flask import Blueprint, render_template, request, redirect, session
from database.db import db
from database.models import Personaggio

characters_bp = Blueprint("characters", __name__)

def require_login():
    if "user_id" not in session:
        return redirect("/login")

@characters_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    personaggi = Personaggio.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "dashboard.html",
        personaggi=personaggi
    )


@characters_bp.route("/personaggi/crea", methods=["GET", "POST"])
def crea_personaggio():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        nome = request.form["nome"]
        classe = request.form["classe"]
        personaggio = Personaggio(
            nome=nome,
            classe=classe,
            user_id=session["user_id"]
        )

        db.session.add(personaggio)
        db.session.commit()
        return redirect("/dashboard")

    return render_template("crea_personaggio.html")
```

---

# Template di base

## templates/layout.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>GDR</title>
</head>
<body>
    <nav>
        <a href="/dashboard">Dashboard</a>
        <a href="/logout">Logout</a>
    </nav>
    <hr>
    {% block content %}{% endblock %}
</body>
</html>
```

---

## templates/login.html

```html
{% extends "layout.html" %}
{% block content %}
<h2>Login</h2>
<form method="POST">
<input name="username" placeholder="username">
<input name="password" type="password">
<button type="submit">Login</button>
</form>
<a href="/signup">Registrati</a>
{% endblock %}
```

---

## templates/signup.html

```html
{% extends "layout.html" %}
{% block content %}

<h2>Registrazione</h2>

<form method="POST">
<input name="username">
<input name="password" type="password">
<button type="submit">Registrati</button>
</form>

{% endblock %}
```

---

## templates/dashboard.html

```html
{% extends "layout.html" %}
{% block content %}

<h2>I tuoi personaggi</h2>
<ul>
{% for p in personaggi %}
<li>{{p.nome}} - {{p.classe}} - lvl {{p.livello}}</li>
{% endfor %}
</ul>

<a href="/personaggi/crea">Nuovo personaggio</a>
{% endblock %}
```

---

# Database seed (facoltativo)

## database/seed.py

```python
from database.db import db
from database.models import User
from werkzeug.security import generate_password_hash


def seed():

    user = User(
        username="demo",
        password=generate_password_hash("demo")
    )

    db.session.add(user)

    db.session.commit()
```

---

# Funzionalità coperte

| Funzione         | Route            | Protezione |
| ---------------- | ---------------- | ---------- |
| Registrazione    | /signup          | pubblica   |
| Login            | /login           | pubblica   |
| Logout           | /logout          | login      |
| Dashboard        | /dashboard       | login      |
| Lista personaggi | /personaggi      | login      |
| Crea personaggio | /personaggi/crea | login      |

---

# Sicurezza consigliata

Password:

```bash
generate_password_hash()
check_password_hash()
```

Sessioni:
bash
session["user_id"]
session["username"]
```

---

# Possibili estensioni (v1.1+)

Sistema completo RPG:

### Inventario

```bash
User → Personaggi → Inventario → Oggetti
```

### Missioni

```bash
Missione
Ambiente
Enemy
Reward
```

### Sistema combattimento

```bash
Turn-based battle
AI nemici
Log battaglia
```

---

# Evoluzione architetturale futura

Architettura moderna:

```bash
React Frontend
     ↓
Flask REST API
     ↓
Game Engine Services
     ↓
PostgreSQL Database
```

---

# Conclusione

Questa integrazione introduce:

* autenticazione utenti
* persistenza database
* gestione personaggi
* struttura modulare Flask

e rappresenta una base solida per evolvere il progetto **GDR Web RPG** in una piattaforma completa.
