import random

from flask import redirect, render_template, request, session, url_for, flash
from flask_login import login_required, current_user

from . import battle_bp
from auth.models import db
from characters.utils import CharacterManager
from inventory.utils import InventoryManager
from gioco.missione import Missione
from gioco.personaggio import Personaggio
from gioco.inventario import Inventario
from gioco.schemas.missione import MissioniSchema
from gioco.schemas.personaggio import PersonaggioSchema
from gioco.schemas.inventario import InventarioSchema
from config import load_leaderboard, update_leaderboard


missione_schema = MissioniSchema()
personaggio_schema = PersonaggioSchema()
inventario_schema = InventarioSchema()


def _load_owned_characters():
    owned_ids = CharacterManager.filter_owned_characters(current_user.character_ids or [])
    return CharacterManager.load_multiple_characters_json(owned_ids)


def _is_alive(personaggio: Personaggio) -> bool:
    return personaggio.salute > 0


def _ensure_battle_state():
    state = session.get("battle_state")
    if not state:
        return None
    return state


def _save_battle_state(state):
    session["battle_state"] = state
    session.modified = True


def _build_turn_order(pc_ids, npc_ids):
    # Prefix IDs to avoid collisions between players and enemies.
    ordine = [f"pc:{x}" for x in pc_ids] + [f"npc:{x}" for x in npc_ids]
    random.shuffle(ordine)
    return ordine


def _t(it_text, en_text):
    return en_text if session.get("lang") == "en" else it_text


def _resolve_battle_turn(state):
    pcs = personaggio_schema.load(state["pcs"], many=True)
    npcs = personaggio_schema.load(state["npcs"], many=True)
    missione = missione_schema.load(state["missione"])
    ambiente = missione.ambiente

    tutti = pcs + npcs
    ordine = state["turn_order"]
    index = state.get("turn_index", 0)
    logs = state.get("logs", [])

    if not ordine:
        ordine = _build_turn_order([p.id for p in pcs], [n.id for n in npcs])
        index = 0

    actor = None
    actor_is_npc = False
    checked = 0
    while checked < len(ordine):
        actor_key = str(ordine[index % len(ordine)])
        if ":" in actor_key:
            actor_side, actor_id = actor_key.split(":", 1)
        else:
            # Backward compatibility for old sessions.
            actor_side, actor_id = "pc", actor_key

        if actor_side == "npc":
            actor = next((x for x in npcs if str(x.id) == str(actor_id)), None)
            actor_is_npc = True
        else:
            actor = next((x for x in pcs if str(x.id) == str(actor_id)), None)
            actor_is_npc = False

        if actor and _is_alive(actor):
            break
        index = (index + 1) % len(ordine)
        checked += 1

    if not actor or not _is_alive(actor):
        return pcs, npcs, logs, True, False, state

    if actor_is_npc:
        targets = [p for p in pcs if _is_alive(p)]
    else:
        targets = [n for n in npcs if _is_alive(n)]

    logs.append(_t(
        f"Turno {state.get('round', 0) + 1}: {actor.nome} agisce.",
        f"Turn {state.get('round', 0) + 1}: {actor.nome} acts."
    ))

    if targets:
        target = random.choice(targets)
        danno = actor.attacca(ambiente.modifica_attacco(actor))
        if danno > 0:
            target.subisci_danno(danno)
            logs.append(_t(
                f"{actor.nome} colpisce {target.nome} per {danno} danni.",
                f"{actor.nome} hits {target.nome} for {danno} damage."
            ))
            if target.sconfitto():
                logs.append(_t(
                    f"{target.nome} è stato sconfitto.",
                    f"{target.nome} has been defeated."
                ))
        else:
            logs.append(_t(
                f"{actor.nome} fallisce l'attacco contro {target.nome}.",
                f"{actor.nome} misses the attack against {target.nome}."
            ))
    else:
        logs.append(_t(
            f"Nessun bersaglio valido per {actor.nome}.",
            f"No valid target for {actor.nome}."
        ))

    index = (index + 1) % len(ordine)
    state["round"] = state.get("round", 0) + 1

    pc_alive = [p for p in pcs if _is_alive(p)]
    npc_alive = [n for n in npcs if _is_alive(n)]
    battaglia_finita = not pc_alive or not npc_alive
    vittoria = bool(pc_alive) and not npc_alive

    if battaglia_finita and vittoria:
        _assign_rewards(missione, pcs)
        logs.append(_t("Vittoria! Premi assegnati.", "Victory! Rewards assigned."))
    elif battaglia_finita:
        logs.append(_t("Sconfitta! I nemici hanno vinto.", "Defeat! Enemies won."))

    state["pcs"] = personaggio_schema.dump(pcs, many=True)
    state["npcs"] = personaggio_schema.dump(npcs, many=True)
    state["logs"] = logs
    state["turn_order"] = ordine
    state["turn_index"] = index

    _persist_characters(pcs)
    return pcs, npcs, logs, battaglia_finita, vittoria, state


def _persist_characters(personaggi):
    for pg in personaggi:
        CharacterManager.save_character_json(personaggio_schema.dump(pg))


def _assign_rewards(missione: Missione, pcs):
    if not pcs or not missione.premi:
        return

    inventories = []
    for pg in pcs:
        inv_data = InventoryManager.load_inventory_json(str(pg.id))
        if not inv_data:
            continue
        inventories.append(inventario_schema.load(inv_data))

    if not inventories:
        return

    for premio in missione.premi:
        inv = random.choice(inventories)
        inv.aggiungi_oggetto(premio)

    for inv in inventories:
        InventoryManager.save_inventory_json(inv)


def _finalize_battle(pcs, npcs, vittoria):
    alive_pcs = [pg for pg in pcs if _is_alive(pg)]
    dead_pcs = [pg for pg in pcs if not _is_alive(pg)]
    # Defensive deduplication by ID to avoid duplicate removals/log lines.
    dead_pcs = list({str(pg.id): pg for pg in dead_pcs}.values())

    # Rimuove personaggi sconfitti dal sistema
    current_ids = [str(cid) for cid in (current_user.character_ids or [])]
    changed_ids = False
    for morto in dead_pcs:
        morto_id = str(morto.id)
        CharacterManager.delete_character_json(morto_id)
        InventoryManager.delete_inventory_json(morto_id)
        if morto_id in current_ids:
            current_ids.remove(morto_id)
            changed_ids = True

    if changed_ids:
        current_user.character_ids = current_ids
        db.session.commit()

    # Aggiorna classifica
    user_id = str(current_user.id)
    stats = load_leaderboard(user_id) or {}
    partite_giocate = int(stats.get("partite_giocate", 0)) + 1
    partite_vinte = int(stats.get("partite_vinte", 0)) + (1 if vittoria else 0)
    punteggio = int(stats.get("punteggio", 0))

    nemici_sconfitti = len([n for n in npcs if not _is_alive(n)])
    penalty_morti = len(dead_pcs) * 5
    bonus_vittoria = 20 if vittoria else 0
    bonus_sopravvissuti = len(alive_pcs) * 3
    punteggio_delta = (nemici_sconfitti * 8) + bonus_vittoria + bonus_sopravvissuti - penalty_morti

    update_leaderboard(
        user_id,
        {
            "nome": current_user.nome,
            "partite_giocate": partite_giocate,
            "partite_vinte": partite_vinte,
            "punteggio": punteggio + punteggio_delta
        }
    )

    return alive_pcs, dead_pcs, punteggio_delta


#---------------------------SHOW_INVENTORY--------------------------------
@battle_bp.route('/show_inventory', methods=['GET', 'POST'])
@login_required
def show_inventory():
    return redirect(url_for('inventory.inventory'))


#---------------------------BEGIN THE BATTLE------------------------------
@battle_bp.route('/begin_battle', methods=['GET', 'POST'])
@login_required
def begin_battle():
    missione_data = session.get("missione")
    if not missione_data:
        flash("Seleziona prima una missione.", "warning")
        return redirect(url_for("mission.select_mission"))

    missione = missione_schema.load(missione_data)
    personaggi = _load_owned_characters()

    if request.method == 'POST':
        selected_ids = request.form.getlist("selected_chars")
        if not selected_ids:
            flash("Seleziona almeno un personaggio.", "warning")
            return redirect(url_for("battle.begin_battle"))

        selected_dicts = [p for p in personaggi if str(p["id"]) in selected_ids]
        if not selected_dicts:
            flash("Personaggi selezionati non validi.", "danger")
            return redirect(url_for("battle.begin_battle"))

        state = {
            "missione": missione_schema.dump(missione),
            "pcs": selected_dicts,
            "npcs": personaggio_schema.dump(missione.nemici, many=True),
            "logs": [],
            "round": 0,
            "turn_order": _build_turn_order(
                [p["id"] for p in selected_dicts],
                [str(n.id) for n in missione.nemici]
            ),
            "turn_index": 0
        }
        _save_battle_state(state)
        return redirect(url_for("battle.test_battle"))

    return render_template(
        "begin_battle.html",
        personaggi=personaggi,
        missione_corrente=missione
    )


#---------------------------SELECT_CHAR-----------------------------------
@battle_bp.route('/select_char', methods=['GET', 'POST'])
@login_required
def select_char():
    return redirect(url_for("battle.begin_battle"))


#---------------------------TEST BATTLE-----------------------------------
@battle_bp.route('/test_battle', methods=['GET', 'POST'])
@login_required
def test_battle():
    state = _ensure_battle_state()
    if not state:
        flash("Nessuna battaglia in corso. Inizia una nuova battaglia.", "warning")
        return redirect(url_for("battle.begin_battle"))

    missione = missione_schema.load(state["missione"])
    pcs, npcs, logs, battaglia_finita, vittoria, state = _resolve_battle_turn(state)
    _save_battle_state(state)

    if battaglia_finita:
        alive_pcs, dead_pcs, delta = _finalize_battle(pcs, npcs, vittoria)
        if dead_pcs:
            logs.append(
                _t("Personaggi rimossi dopo la battaglia: ",
                   "Characters removed after battle: ")
                + ", ".join(pg.nome for pg in dead_pcs)
            )
        logs.append(_t(f"Classifica aggiornata. Punteggio partita: {delta:+d}.",
                       f"Leaderboard updated. Match score: {delta:+d}."))
        pcs = alive_pcs
        session.pop("battle_state", None)

    return render_template(
        "battle.html",
        battaglia_finita=battaglia_finita,
        vittoria=vittoria,
        messaggi=logs,
        personaggi=pcs,
        nemici=npcs,
        missione=missione,
        pc_vivi=[p for p in pcs if _is_alive(p)],
        npc_vivi=[n for n in npcs if _is_alive(n)]
    )

