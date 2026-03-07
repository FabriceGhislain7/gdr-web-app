# GDR (Gioco di Ruolo) — Web Role Playing Game (Flask)

GDR (Gioco di Ruolo) is a web-based **Role Playing Game (RPG)** built with Flask, designed to explore modular backend architecture and object-oriented design in a turn-based game environment.

The application implements core RPG mechanics including character creation, mission selection, combat systems, inventory management, and game state persistence.

This project represents an early implementation of a **web-based RPG engine**, with a focus on backend logic and modular game design.

---

# Features

The application includes several gameplay systems:

* Character creation and management
* Mission selection and environment system
* Turn-based combat mechanics
* Inventory and item effects
* Game state saving and loading
* Modular Flask architecture using Blueprints

The project separates **game engine logic** from the **web interface**, allowing easier future expansion and refactoring.

---

# Architecture Overview

The application follows a modular layered architecture.

```text
Web Interface (Flask Routes)
        │
        ▼
Application Layer
        │
        ▼
Game Engine Logic
        │
        ▼
Data Persistence (JSON / Session)
```

Key design goals include:

* modular structure
* separation of concerns
* reusable gameplay components
* extensibility for new game mechanics

---

# Project Structure

```
gdr-web-app/
│
├── app.py
├── requirements.txt
│
├── static/
├── templates/
│
├── utils/
│
├── gioco/          # Core game engine
│
├── battle/         # Battle system
├── characters/     # Character management
├── inventory/      # Inventory system
├── mission/        # Mission logic
├── environment/    # Game environments
│
└── data/           # Save files
```

Each module isolates a specific part of the gameplay logic.

---

# Technology Stack

Backend framework:

* Flask
* Flask-Session
* Flask-Login
* Flask-SQLAlchemy

Core technologies:

* Python
* Jinja2 templates
* JSON persistence

---

# Gameplay Systems

The game engine includes several gameplay subsystems.

### Character System

Handles:

* character classes
* attributes
* health and abilities

### Mission System

Defines playable missions and environments.

### Combat System

Implements turn-based battle mechanics including:

* player turns
* enemy actions
* combat resolution

### Inventory System

Manages:

* item storage
* item effects
* equipment management

---

# Running the Application

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Windows

```
venv\Scripts\activate
```

Linux / Mac

```
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

---

# Documentation

Additional technical documentation is available in the `docs` folder.

* `docs/ARCHITECTURE.md`
* `docs/GAME_ENGINE.md`
* `docs/DEVELOPMENT.md`

---

# Future Evolution

This project will evolve into a more advanced architecture:

**GDR RPG Platform — Flask API + React Frontend**

The future version will include:

* API-first backend architecture
* React frontend interface
* database persistence
* improved combat and mission systems
* modular RPG engine expansion

---

# Author

Fabrice Ghislain Tebou
GitHub
[https://github.com/FabriceGhislain7](https://github.com/FabriceGhislain7)


