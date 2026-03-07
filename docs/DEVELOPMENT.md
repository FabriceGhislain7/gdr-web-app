# GDR (Gioco di Ruolo) — Development Guide

This document provides guidelines for developing, extending, and maintaining the **GDR (Gioco di Ruolo)** web application.

It describes the development environment, coding conventions, and architectural practices used in the project.

---

# Development Environment

The project requires Python 3.9 or newer.

Recommended tools:

* Python virtual environment
* Git for version control
* Visual Studio Code or similar IDE

---

# Project Setup

Clone the repository:

```bash
git clone <repository-url>
cd gdr-web-app
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment.

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
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

# Development Workflow

Recommended development process:

1. Create a feature branch
2. Implement the feature
3. Test locally
4. Commit changes
5. Merge into the main branch

Example:

```bash
git checkout -b feature/new-mission-system
```

---

# Code Organization

The project is structured around **functional modules** and a **core game engine**.

Main directories:

```text
gioco/        → core game logic
battle/       → combat system routes
characters/   → character management
inventory/    → inventory system
mission/      → mission system
environment/  → environment selection
utils/        → shared utilities
```

Game mechanics are implemented inside the **`gioco` module**, while Flask blueprints expose functionality through HTTP routes.

---

# Adding a New Gameplay Feature

To introduce a new gameplay feature:

1. Implement the core logic inside `gioco/`
2. Create or extend a Flask blueprint
3. Add routes to expose the feature
4. Create templates for the interface
5. Update session management if needed

Example flow:

```text
Game Logic (gioco/)
      ↓
Blueprint Routes
      ↓
Template Rendering
```

---

# Serialization of Game Objects

Game state is stored in session or saved as JSON.

Important classes implement:

```python
def to_dict(self):
    ...
```

and

```python
@classmethod
def from_dict(cls, data):
    ...
```

This approach allows objects such as characters, missions, or inventory items to be stored and reconstructed easily.

---

# Game State Management

Game state is stored using Flask sessions.

Stored data may include:

* active characters
* inventory items
* current mission
* battle state

For exporting save files, JSON serialization is used.

---

# Logging

Logging utilities are located in:

```text
utils/log.py
```

Logging helps track:

* game events
* errors
* debugging information

Future improvements may include structured logging.

---

# Templates and Frontend

The application uses **Jinja2 templates**.

Templates are located in:

```text
templates/
```

Base layout:

```text
layout.html
```

Each page extends the base layout.

Example:

```text
menu.html
battle.html
inventory.html
```

---

# Static Assets

Static resources are stored in:

```text
static/
```

Includes:

* CSS styles
* JavaScript files
* images
* environment backgrounds

---

# Extending the Game Engine

New gameplay elements can be added by introducing new classes.

Examples include:

* new character classes
* new enemy types
* new items
* new environments
* new mission types

The modular architecture allows extending the game engine without modifying unrelated modules.

---

# Known Limitations

Current limitations include:

* no persistent database
* limited UI styling
* no automated tests
* game state stored only in session or JSON

---

# Future Development

Planned improvements include:

* integration with a database using Flask-SQLAlchemy
* authentication system with Flask-Login
* improved frontend styling (Bootstrap or modern UI)
* automated tests
* separation between backend and frontend

Future versions of the project will evolve into a **modern API-based architecture with a React frontend**.

---

# Development Philosophy

The project focuses on:

* learning modular backend architecture
* implementing object-oriented gameplay systems
* exploring web-based game development

The codebase is designed to remain **simple, readable, and extensible**.


