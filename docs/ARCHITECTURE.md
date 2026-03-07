# GDR (Gioco di Ruolo) — System Architecture

This document describes the internal architecture of **GDR (Gioco di Ruolo)**, a web-based role playing game built with Flask.

The goal of the architecture is to separate the **web interface**, **application logic**, and **game engine mechanics**, allowing the system to remain modular and extensible.

---

# Architectural Overview

The application follows a layered architecture where each component has a well-defined responsibility.

```
User Browser
      │
      ▼
Flask Web Interface (Routes & Templates)
      │
      ▼
Application Layer (Game Flow Management)
      │
      ▼
Game Engine (Core Gameplay Logic)
      │
      ▼
Data Persistence (Session / JSON Save Files)
```

This structure ensures that gameplay mechanics remain independent from the web interface.

---

# System Components

The system is composed of several main components:

* Web Interface
* Game Engine
* Gameplay Modules
* Utilities
* Data Persistence

Each component is implemented as an isolated module.

---

# Web Layer

The web layer is responsible for:

* handling HTTP requests
* rendering templates
* interacting with the game engine

The application uses **Flask Blueprints** to organize routes by functionality.

Main entry point:

```
app.py
```

Responsibilities:

* Flask application initialization
* configuration setup
* blueprint registration
* session management

Example blueprint registration:

```python
app.register_blueprint(gioco)
app.register_blueprint(inventory)
app.register_blueprint(mission)
```

---

# Blueprint Architecture

Each gameplay domain is implemented as a Flask Blueprint.

Blueprints allow:

* modular routing
* separation of functional domains
* improved maintainability

Modules include:

```
battle/
characters/
inventory/
mission/
environment/
```

Each module exposes its own routes and handles specific gameplay features.

---

# Game Engine Layer

The core gameplay logic is implemented inside the `gioco/` module.

This module represents the **game engine** and contains the classes that define the behavior of the game.

Core components include:

```
personaggio.py
missione.py
inventario.py
oggetto.py
scontro.py
strategy.py
ambiente.py
```

Responsibilities:

* define gameplay mechanics
* manage game entities
* control combat flow
* manage interactions between characters and objects

---

# Gameplay Systems

The game engine contains several subsystems.

### Character System

Manages:

* character classes
* character attributes
* player and enemy entities

Main class:

```
Personaggio
```

---

### Combat System

Implemented in:

```
scontro.py
```

Handles:

* turn-based combat logic
* player actions
* enemy responses
* battle resolution

---

### Mission System

Implemented in:

```
missione.py
```

Responsibilities:

* mission definitions
* mission objectives
* mission selection logic

---

### Inventory System

Implemented in:

```
inventario.py
```

Handles:

* item storage
* item effects
* character equipment

---

### Environment System

Implemented in:

```
ambiente.py
```

Defines:

* environments
* contextual mission settings

---

# Data Persistence

Game state persistence is implemented using:

* Flask sessions
* JSON save files

Location:

```
data/
```

Game objects are serialized into dictionaries before saving.

Example:

```python
def to_dict(self):
    ...
```

Objects can be reconstructed using:

```python
@classmethod
def from_dict(cls, data):
    ...
```

This approach ensures that game state can be stored and restored reliably.

---

# Utilities Layer

Shared utility modules are located in:

```
utils/
```

Modules include:

```
log.py
messaggi.py
salvataggio.py
```

Responsibilities include:

* logging
* message formatting
* game state serialization

---

# Template System

The user interface is implemented using **Jinja2 templates**.

Location:

```
templates/
```

Main templates include:

```
layout.html
menu.html
create_char.html
select_mission.html
battle.html
inventory.html
guide_game.html
```

Templates render the current game state and provide interaction with the player.

---

# Static Resources

Static assets are stored in:

```
static/
```

Resources include:

* CSS stylesheets
* JavaScript scripts
* images
* environment assets

---

# Design Principles

The architecture of the system follows several software engineering principles.

### Modular Design

Each gameplay feature is implemented in an isolated module.

### Separation of Concerns

Game logic is separated from the web interface.

### Object-Oriented Design

Game entities are implemented using Python classes.

### Extensibility

The architecture allows easy addition of:

* new missions
* new character classes
* new environments
* new items

---

# Future Architecture Evolution

The current system represents the initial version of the GDR game engine.

Future development will introduce a new architecture:

**GDR RPG Platform — Flask API + React Frontend**

The new architecture will include:

```
React Frontend
      │
      ▼
Flask REST API
      │
      ▼
Game Engine Services
      │
      ▼
Database Persistence
```

This evolution will separate the frontend from the backend and allow better scalability.

---

# Summary

The architecture of **GDR (Gioco di Ruolo)** is designed to demonstrate:

* modular Flask application design
* object-oriented game engine development
* separation between gameplay logic and web interface

The project provides a foundation for further evolution into a modern **API-driven RPG platform**.

