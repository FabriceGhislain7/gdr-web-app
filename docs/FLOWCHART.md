# GDR (Gioco di Ruolo) — System Flow Diagrams

This document illustrates the main execution flows and architecture of the **GDR (Gioco di Ruolo)** web RPG application.

The diagrams describe how the system connects:

- the user interface
- Flask application routes
- the game engine
- gameplay systems
- persistence mechanisms

---

# System Architecture Diagram

This diagram shows the overall interaction between the **web interface**, **Flask backend**, and the **game engine**.

```mermaid
flowchart TD

User[User Browser]

FlaskApp[Flask Application]

Blueprints[Flask Blueprints]

Templates[Jinja Templates]

GameEngine[Game Engine Module]

Characters[Character System]

Combat[Combat System]

Inventory[Inventory System]

Missions[Mission System]

Environment[Environment System]

Persistence[(Session / JSON Save)]

User --> FlaskApp

FlaskApp --> Blueprints

Blueprints --> Templates

Blueprints --> GameEngine

GameEngine --> Characters
GameEngine --> Combat
GameEngine --> Inventory
GameEngine --> Missions
GameEngine --> Environment

GameEngine --> Persistence
````

---

# Layered Architecture Diagram

This diagram represents the **layered structure** of the application.

```mermaid
flowchart TB

subgraph Presentation Layer
Browser[User Browser]
Templates[Jinja Templates]
Static[Static Assets]
end

subgraph Web Layer
FlaskApp[Flask App]
Routes[Blueprint Routes]
end

subgraph Application Layer
GameFlow[Game Flow Controller]
SessionManager[Session Management]
end

subgraph Game Engine Layer
Characters[Character System]
Combat[Combat Engine]
Inventory[Inventory System]
Missions[Mission Logic]
Environment[Environment System]
Items[Item System]
end

subgraph Persistence Layer
Session[(Flask Session)]
JSON[(JSON Save Files)]
end

Browser --> FlaskApp

FlaskApp --> Routes
Routes --> Templates
Routes --> GameFlow

GameFlow --> Characters
GameFlow --> Combat
GameFlow --> Inventory
GameFlow --> Missions
GameFlow --> Environment
GameFlow --> Items

GameFlow --> SessionManager

SessionManager --> Session
SessionManager --> JSON
```

---

# Internal Module Architecture

This diagram reflects the **real project structure**.

```mermaid
flowchart LR

app[app.py]

subgraph gioco
personaggio[personaggio.py]
missione[missione.py]
inventario[inventario.py]
oggetto[oggetto.py]
scontro[scontro.py]
strategy[strategy.py]
ambiente[ambiente.py]
classi[classi.py]
end

subgraph blueprints
battle[battle module]
characters[characters module]
inventory[inventory module]
mission[mission module]
environment[environment module]
end

subgraph utils
log[log.py]
messaggi[messaggi.py]
salvataggio[salvataggio.py]
end

subgraph interface
templates[templates]
static[static assets]
end

app --> battle
app --> characters
app --> inventory
app --> mission
app --> environment

battle --> scontro
characters --> personaggio
inventory --> inventario
mission --> missione
environment --> ambiente

personaggio --> classi
inventario --> oggetto
scontro --> strategy

battle --> templates
characters --> templates
inventory --> templates
mission --> templates
environment --> templates

templates --> static

scontro --> utils
personaggio --> utils
missione --> utils
```

---

# Gameplay Flow Diagram

This diagram describes the **player gameplay progression**.

```mermaid
flowchart LR

Start[Start Game]

Menu[Main Menu]

CreateChar[Character Creation]

LoadGame[Load Game]

SelectMission[Select Mission]

Battle[Battle System]

Inventory[Inventory Management]

SaveGame[Save Game]

EndGame[End Mission]

Start --> Menu

Menu --> CreateChar
Menu --> LoadGame

CreateChar --> SelectMission
LoadGame --> SelectMission

SelectMission --> Battle

Battle --> Inventory
Inventory --> Battle

Battle --> EndGame

EndGame --> SaveGame
SaveGame --> Menu
```

---

# Combat Flow Diagram

This diagram illustrates the **turn-based combat logic**.

```mermaid
flowchart TD

StartBattle[Battle Start]

PlayerTurn[Player Turn]

ChooseAction[Choose Action]

Attack[Attack]

Defend[Defend]

UseItem[Use Item]

ProcessAction[Process Action]

EnemyTurn[Enemy Turn]

DamageCalc[Damage Calculation]

UpdateHealth[Update Health]

CheckEnd[Check Battle Result]

Victory[Enemy Defeated]

Defeat[Player Defeated]

Continue[Next Turn]

StartBattle --> PlayerTurn

PlayerTurn --> ChooseAction

ChooseAction --> Attack
ChooseAction --> Defend
ChooseAction --> UseItem

Attack --> ProcessAction
Defend --> ProcessAction
UseItem --> ProcessAction

ProcessAction --> EnemyTurn

EnemyTurn --> DamageCalc
DamageCalc --> UpdateHealth

UpdateHealth --> CheckEnd

CheckEnd --> Victory
CheckEnd --> Defeat
CheckEnd --> Continue

Continue --> PlayerTurn
```

---

# Save / Load Game Flow

This diagram describes how the game state is stored and restored.

```mermaid
flowchart LR

GameState[Game State]

Serialize[Serialize Objects]

Session[(Flask Session)]

JSON[(JSON Save File)]

Deserialize[Deserialize Objects]

RestoreState[Restore Game State]

GameState --> Serialize

Serialize --> Session
Serialize --> JSON

Session --> Deserialize
JSON --> Deserialize

Deserialize --> RestoreState
```

---

# Summary

These diagrams illustrate the main structural elements of the **GDR RPG system**:

* modular Flask architecture
* layered application structure
* object-oriented game engine
* turn-based combat flow
* persistent game state management

The system is designed to remain **modular, extensible, and maintainable**, allowing future evolution toward a **Flask API + React frontend architecture**.

