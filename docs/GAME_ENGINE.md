# GDR (Gioco di Ruolo) — Game Engine Design

This document describes the internal design of the **GDR (Gioco di Ruolo)** game engine.

The engine implements the core mechanics of a role-playing game, including characters, missions, combat systems, inventory management, and environmental contexts.

The goal of the engine is to separate **gameplay logic** from the web interface, allowing the game system to remain modular and extensible.

---

# Game Engine Overview

The engine is implemented inside the `gioco/` module and represents the central logic layer of the application.

Main components include:

```text
personaggio.py
missione.py
inventario.py
oggetto.py
scontro.py
strategy.py
ambiente.py
classi.py
```

Each module represents a specific gameplay system.

---

# Core Game Entities

The engine is built around several core entities.

### Character

Implemented in:

```text
personaggio.py
```

The character class represents both players and enemies.

Responsibilities include:

* health management
* attributes and abilities
* interaction with inventory
* combat participation

Typical attributes include:

* health points
* attack strength
* defense
* character class

---

### Character Classes

Defined in:

```text
classi.py
```

Character classes define different gameplay styles.

Examples may include:

* warrior
* mage
* ranger

Each class may define specific attributes or abilities.

---

# Combat System

The combat system is implemented in:

```text
scontro.py
```

The system follows a **turn-based combat model**.

Basic combat flow:

```text
Player Turn
     ↓
Enemy Turn
     ↓
Battle Resolution
```

Combat logic includes:

* attack calculations
* damage resolution
* health updates
* victory or defeat conditions

The combat system is designed to be easily extended with new mechanics.

---

# Combat Strategy System

Implemented in:

```text
strategy.py
```

The strategy module defines how actions are executed during combat.

Possible strategies may include:

* attack
* defend
* use item

This allows introducing different behaviors without modifying the combat engine.

---

# Mission System

Implemented in:

```text
missione.py
```

The mission system defines the objectives and environments of the game.

Responsibilities include:

* mission generation
* mission selection
* mission completion logic

Missions may include:

* combat encounters
* exploration tasks
* environment challenges

---

# Environment System

Implemented in:

```text
ambiente.py
```

The environment defines the context in which missions occur.

Examples may include:

* forest
* dungeon
* village

Environments may influence gameplay conditions.

---

# Inventory System

Implemented in:

```text
inventario.py
```

The inventory system manages the items owned by characters.

Responsibilities include:

* storing items
* equipping items
* using consumables

The system interacts closely with the character and combat systems.

---

# Item System

Implemented in:

```text
oggetto.py
```

Items define special gameplay effects.

Examples include:

* healing potions
* weapons
* defensive equipment

Items may influence:

* character attributes
* combat outcomes

---

# Game State Management

The engine supports saving and restoring the game state.

Game objects are serialized into dictionaries using:

```python
def to_dict(self):
```

and reconstructed using:

```python
@classmethod
def from_dict(cls, data):
```

This allows storing game state in:

* session
* JSON save files

---

# Game Loop Concept

Although the application is web-based, the engine follows a conceptual game loop.

```text
Player Action
      ↓
Game Engine Processes Action
      ↓
Update Game State
      ↓
Render Updated Interface
```

This structure allows the engine to behave similarly to traditional game engines.

---

# Design Principles

The game engine follows several design principles.

### Object-Oriented Design

Game entities are implemented as Python classes.

### Modularity

Each gameplay system is isolated in its own module.

### Extensibility

New mechanics can be introduced without rewriting existing systems.

Examples include:

* new items
* new character classes
* new mission types
* new environments

---

# Future Engine Evolution

The current engine is embedded inside a Flask web application.

Future versions will evolve into a **service-based architecture**.

Planned evolution:

```text
React Frontend
      ↓
Flask API
      ↓
Game Engine Services
      ↓
Database Persistence
```

This architecture will allow:

* real-time gameplay interactions
* modern UI development
* scalable backend services

---

# Purpose of This Engine

The GDR engine demonstrates:

* object-oriented game design
* modular gameplay systems
* integration between game logic and web applications

It provides a foundation for future development of a **full RPG platform**.


