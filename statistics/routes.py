from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import current_user, login_required
from . import statistics_bp
import os
import json
import csv
from functools import lru_cache
from config import BASE_DIR, DATA_DIR_SAVE, DATA_DIR_PGS, load_leaderboard


# Home / menu principale
@statistics_bp.route('/statistics')
def show_statistics():
    """
    Funzione di ritorno della pagina principale
    """

    users_stats = load_leaderboard()
    # utilizzo di 'sorted'
    # - un elemento iterabile ad esempio 'content.items'
    # - con 'content.items' ottengo una lista di tuple dal dizionario
    # - 'key=lambda x: x[1]['punteggio']' vuol dire per ogni
    # elemento x, prendi il punteggio corrispondente
    users_stats_sorted = sorted(
        users_stats.items(),
        key=lambda x: x[1]['punteggio'],
        reverse=True
        )
    # Mostra in classifica solo utenti che hanno realmente giocato almeno una partita
    users_stats_sorted = [
        item for item in users_stats_sorted
        if int(item[1].get('partite_giocate', 0)) > 0
    ]
    if current_user.is_authenticated:
        has_personaggi = False
        has_missioni = False
        # controlla se ci sono personaggi e missioni nel file json
        for filename in os.listdir(DATA_DIR_PGS):
            if filename.endswith('.json'):
                full_path = os.path.join(DATA_DIR_PGS, filename)
                try:
                    with open(full_path, 'r', encoding='utf-8') as file:
                        personaggi = json.load(file)
                        for char_id in current_user.character_ids:
                            if personaggi['id'] == char_id:
                                has_personaggi = True
                                break
                except (json.JSONDecodeError, KeyError, IOError) as e:
                    # Salta i file JSON corrotti o malformati
                    print(f"Errore nel caricamento del file {filename}: {e}")
                    continue
        file_path_save = os.path.join(DATA_DIR_SAVE, "salvataggio.json")
        if os.path.exists(file_path_save):
            try:
                with open(file_path_save, 'r', encoding='utf-8') as file:
                    salvataggio = json.load(file)
                    if 'missione' in salvataggio:
                        has_missioni = True
            except (json.JSONDecodeError, IOError) as e:
                # Gestisce errori nel file di salvataggio
                print(f"Errore nel caricamento del file di salvataggio: {e}")
                has_missioni = False

            can_select_char = has_personaggi and has_missioni

            return render_template(
                'statistics.html',
                can_select_char=can_select_char,
                has_missioni=has_missioni,
                users_stats_sorted=users_stats_sorted
                )

    return render_template('statistics.html', users_stats_sorted=users_stats_sorted)


@statistics_bp.route('/analytics_dashboard')
def analytics_dashboard():
    return redirect(url_for('statistics.analytics_data_analyst'))


def _to_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value, default=0):
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _percentage(numerator, denominator):
    if denominator <= 0:
        return 0.0
    return round((numerator / denominator) * 100, 2)


@lru_cache(maxsize=1)
def _load_dataset_rows(dataset_path):
    with open(dataset_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _resolve_dataset_path():
    candidates = [
        os.path.join(BASE_DIR, "data", "big_dataset_gioco.csv"),
        os.path.join(BASE_DIR, "big_dataset_gioco.csv"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def _filter_rows(rows, filters):
    filtered = []
    for row in rows:
        keep = True
        for key, value in filters.items():
            if not value:
                continue
            if str(row.get(key, "")).strip().lower() != str(value).strip().lower():
                keep = False
                break
        if keep:
            filtered.append(row)
    return filtered


def _build_filter_options(rows):
    def uniq(field):
        return sorted({(r.get(field) or "").strip() for r in rows if (r.get(field) or "").strip()})
    return {
        "classe_personaggio": uniq("classe_personaggio"),
        "genere": uniq("genere"),
        "paese": uniq("paese"),
        "tipo_dispositivo": uniq("tipo_dispositivo"),
        "cluster_comportamentale": uniq("cluster_comportamentale")
    }


def _build_analytics_payload_from_rows(rows):
    total_players = len(rows)
    if total_players == 0:
        return {
            "kpis": {},
            "charts": {},
            "tables": {},
            "alerts": []
        }

    total_playtime_minutes = sum(_to_float(r.get("tempo_totale_giocato")) for r in rows)
    total_playtime_hours = round(total_playtime_minutes / 60, 1)
    avg_playtime_hours = round((total_playtime_minutes / total_players) / 60, 2)

    total_battles = sum(_to_int(r.get("numero_battaglie")) for r in rows)
    total_wins = sum(_to_int(r.get("numero_vittorie")) for r in rows)
    total_losses = sum(_to_int(r.get("numero_sconfitte")) for r in rows)
    win_rate = _percentage(total_wins, max(total_wins + total_losses, 1))

    avg_session_minutes = round(
        sum(_to_float(r.get("durata_media_sessione")) for r in rows) / total_players, 2
    )
    avg_daily_sessions = round(
        sum(_to_float(r.get("sessioni_giornaliere_medie")) for r in rows) / total_players, 2
    )

    total_monthly_revenue = round(sum(_to_float(r.get("spesa_mensile")) for r in rows), 2)
    arpu = round(total_monthly_revenue / total_players, 2)
    subscribers = sum(1 for r in rows if _to_int(r.get("abbonamento_attivo")) == 1)
    subscriber_rate = _percentage(subscribers, total_players)

    avg_crash = round(sum(_to_float(r.get("numero_crash")) for r in rows) / total_players, 2)
    avg_bug = round(sum(_to_float(r.get("bug_rilevati")) for r in rows) / total_players, 2)
    avg_latency = round(sum(_to_float(r.get("latency_media")) for r in rows) / total_players, 2)
    avg_satisfaction = round(sum(_to_float(r.get("soddisfazione")) for r in rows) / total_players, 2)

    def _group_count(field_name, top_n=8):
        counts = {}
        for row in rows:
            key = row.get(field_name) or "Unknown"
            counts[key] = counts.get(key, 0) + 1
        ordered = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return {
            "labels": [k for k, _ in ordered],
            "values": [v for _, v in ordered]
        }

    def _group_avg(group_field, value_field, top_n=8):
        sums = {}
        counts = {}
        for row in rows:
            key = row.get(group_field) or "Unknown"
            sums[key] = sums.get(key, 0.0) + _to_float(row.get(value_field))
            counts[key] = counts.get(key, 0) + 1
        avg_items = []
        for key in sums:
            avg_items.append((key, round(sums[key] / max(counts[key], 1), 2)))
        ordered = sorted(avg_items, key=lambda x: x[1], reverse=True)[:top_n]
        return {
            "labels": [k for k, _ in ordered],
            "values": [v for _, v in ordered]
        }

    class_distribution = _group_count("classe_personaggio", top_n=10)
    cluster_distribution = _group_count("cluster_comportamentale", top_n=10)
    device_distribution = _group_count("tipo_dispositivo", top_n=10)
    acquisition_distribution = _group_count("canale_acquisizione", top_n=10)
    active_day_distribution = _group_count("giorno_settimana_attivo", top_n=7)
    satisfaction_by_class = _group_avg("classe_personaggio", "soddisfazione", top_n=10)
    spend_by_cluster = _group_avg("cluster_comportamentale", "spesa_mensile", top_n=10)
    crash_by_device = _group_avg("tipo_dispositivo", "numero_crash", top_n=10)

    sat_band_counts = {
        "Low (1-3)": 0,
        "Medium (4-6)": 0,
        "High (7-8)": 0,
        "Very High (9-10)": 0
    }
    for row in rows:
        score = _to_float(row.get("soddisfazione"))
        if score <= 3:
            sat_band_counts["Low (1-3)"] += 1
        elif score <= 6:
            sat_band_counts["Medium (4-6)"] += 1
        elif score <= 8:
            sat_band_counts["High (7-8)"] += 1
        else:
            sat_band_counts["Very High (9-10)"] += 1

    satisfaction_bands = {
        "labels": list(sat_band_counts.keys()),
        "values": list(sat_band_counts.values())
    }

    top_playtime = sorted(
        rows,
        key=lambda r: _to_float(r.get("tempo_totale_giocato")),
        reverse=True
    )[:10]
    top_spenders = sorted(
        rows,
        key=lambda r: _to_float(r.get("spesa_mensile")),
        reverse=True
    )[:10]

    high_risk_users = [
        r for r in rows
        if _to_float(r.get("soddisfazione")) <= 3
        and _to_float(r.get("giorni_attivi")) <= 60
        and _to_float(r.get("numero_crash")) >= 6
    ][:10]

    alerts = []
    if win_rate < 45:
        alerts.append("Global win rate is low: possible gameplay imbalance.")
    if avg_crash >= 5:
        alerts.append("Average crashes are high: prioritize client stability improvements.")
    if subscriber_rate < 25:
        alerts.append("Subscriber conversion is low: review premium value proposition.")
    if avg_satisfaction < 5:
        alerts.append("Average satisfaction is below threshold: improve UX and retention.")

    return {
        "kpis": {
            "total_players": total_players,
            "total_playtime_hours": total_playtime_hours,
            "avg_playtime_hours": avg_playtime_hours,
            "total_battles": total_battles,
            "win_rate": win_rate,
            "avg_session_minutes": avg_session_minutes,
            "avg_daily_sessions": avg_daily_sessions,
            "monthly_revenue": total_monthly_revenue,
            "arpu": arpu,
            "subscriber_rate": subscriber_rate,
            "avg_crash": avg_crash,
            "avg_bug": avg_bug,
            "avg_latency": avg_latency,
            "avg_satisfaction": avg_satisfaction
        },
        "charts": {
            "class_distribution": class_distribution,
            "cluster_distribution": cluster_distribution,
            "device_distribution": device_distribution,
            "acquisition_distribution": acquisition_distribution,
            "active_day_distribution": active_day_distribution,
            "satisfaction_bands": satisfaction_bands,
            "satisfaction_by_class": satisfaction_by_class,
            "spend_by_cluster": spend_by_cluster,
            "crash_by_device": crash_by_device
        },
        "tables": {
            "top_playtime": [
                {
                    "nome": r.get("nome", "N/A"),
                    "classe": r.get("classe_personaggio", "N/A"),
                    "ore": round(_to_float(r.get("tempo_totale_giocato")) / 60, 2),
                    "soddisfazione": _to_float(r.get("soddisfazione")),
                    "spesa_mensile": _to_float(r.get("spesa_mensile"))
                }
                for r in top_playtime
            ],
            "top_spenders": [
                {
                    "nome": r.get("nome", "N/A"),
                    "classe": r.get("classe_personaggio", "N/A"),
                    "spesa_mensile": _to_float(r.get("spesa_mensile")),
                    "abbonato": "Yes" if _to_int(r.get("abbonamento_attivo")) == 1 else "No",
                    "acquisizione": r.get("canale_acquisizione", "N/A")
                }
                for r in top_spenders
            ],
            "high_risk_users": [
                {
                    "nome": r.get("nome", "N/A"),
                    "giorni_attivi": _to_int(r.get("giorni_attivi")),
                    "soddisfazione": _to_float(r.get("soddisfazione")),
                    "crash": _to_int(r.get("numero_crash")),
                    "cluster": r.get("cluster_comportamentale", "N/A")
                }
                for r in high_risk_users
            ]
        },
        "alerts": alerts
    }


@statistics_bp.route('/analytics_data_analyst')
@login_required
def analytics_data_analyst():
    if not current_user.is_team_member_developer():
        flash("Access restricted to the developer/data analyst team.", "warning")
        return redirect(url_for("gioco.menu"))

    dataset_path = _resolve_dataset_path()
    if not dataset_path:
        flash("Analytics dataset not found.", "danger")
        return redirect(url_for("statistics.show_statistics"))

    if request.args.get("refresh") == "1":
        _load_dataset_rows.cache_clear()

    rows = _load_dataset_rows(dataset_path)
    payload = _build_analytics_payload_from_rows(rows)
    filter_options = _build_filter_options(rows)
    return render_template(
        "analytics_dashboard.html",
        analytics=payload,
        filter_options=filter_options
    )


@statistics_bp.route('/analytics_data_analyst/api')
@login_required
def analytics_data_analyst_api():
    if not current_user.is_team_member_developer():
        return jsonify({"error": "forbidden"}), 403

    dataset_path = _resolve_dataset_path()
    if not dataset_path:
        return jsonify({"error": "dataset_not_found"}), 404

    rows = _load_dataset_rows(dataset_path)
    filters = {
        "classe_personaggio": request.args.get("classe_personaggio", "").strip(),
        "genere": request.args.get("genere", "").strip(),
        "paese": request.args.get("paese", "").strip(),
        "tipo_dispositivo": request.args.get("tipo_dispositivo", "").strip(),
        "cluster_comportamentale": request.args.get("cluster_comportamentale", "").strip()
    }
    filtered = _filter_rows(rows, filters)
    payload = _build_analytics_payload_from_rows(filtered)
    payload["meta"] = {"filtered_count": len(filtered), "total_count": len(rows)}
    return jsonify(payload)


