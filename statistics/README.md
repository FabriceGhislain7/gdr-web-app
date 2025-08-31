# GDR Game Analytics Project

## 1. Project Overview
Questo progetto simula un dataset di utenti di un gioco di ruolo online (GDR) per attività di analisi dei dati e machine learning.  
L'obiettivo è:
- Creare un dataset realistico per esercitazioni di **analisi esplorativa (EDA)**.
- Applicare **preprocessing con gestione dei valori mancanti**.
- Svolgere **feature engineering**.
- Allenare modelli predittivi per churn, spesa o comportamento degli utenti.

Il dataset è generato artificialmente ma rispecchia dinamiche tipiche dei giochi online.

---

## 2. Dataset Description

Il dataset contiene **50.500 osservazioni** e include variabili demografiche, comportamentali e di performance.

| Variabile                  | Descrizione                                                      |
|---------------------------|------------------------------------------------------------------|
| `player_id`              | Identificativo univoco del giocatore                           |
| `nome`                   | Nome fittizio del giocatore                                    |
| `eta`                    | Età del giocatore (alcuni valori mancanti)                     |
| `genere`                 | Sesso del giocatore (M/F, con alcuni missing)                  |
| `paese`                  | Paese di provenienza                                           |
| `città`                  | Città di provenienza                                           |
| `mestiere`               | Professione del giocatore                                      |
| `istruzione`             | Livello di istruzione (alcuni missing)                         |
| `soddisfazione`          | Grado di soddisfazione (1-10)                                  |
| `classe_personaggio`     | Classe del personaggio (Mago, Guerriero, Ladro)                |
| `livello`                | Livello attuale del giocatore (1-100)                          |
| `salute_media`           | Media punti salute (alcuni missing)                            |
| `attacco_medio`          | Media punteggio d'attacco (alcuni missing)                     |
| `destrezza`              | Punteggio di destrezza (1-20)                                  |
| `oggetti_usati`          | Oggetti utilizzati (es. Spada, Scudo)                          |
| `numero_battaglie`       | Numero di battaglie totali                                     |
| `numero_vittorie`        | Vittorie totali                                                |
| `numero_sconfitte`       | Sconfitte totali                                               |
| `tempo_totale_giocato`   | Tempo totale di gioco in minuti                                |
| `crediti_attuali`        | Crediti residui (alcuni missing)                               |
| `spesa_mensile`          | Spesa mensile in valuta di gioco (alcuni missing)              |
| `numero_acquisti`        | Numero di acquisti effettuati                                  |
| `tipo_acquisti`          | Tipologia di acquisti (es. armi, oggetti)                      |
| `abbonamento_attivo`     | Stato abbonamento (0 = No, 1 = Sì)                             |
| `rimborso_totale`        | Importo totale rimborsato                                      |
| `giorni_attivi`          | Giorni attivi nell'ultimo anno                                 |
| `sessioni_giornaliere_medie` | Numero medio di sessioni giornaliere                      |
| `durata_media_sessione`  | Durata media sessione in minuti                                |
| `ora_punta_login`        | Ora del giorno di picco (0-23)                                 |
| `giorno_settimana_attivo`| Giorno più attivo (es. Lunedì)                                  |
| `pausa_media_tra_sessioni`| Pausa media tra sessioni (ore)                                |
| `tipo_dispositivo`       | Dispositivo (PC, Mobile, Tablet)                               |
| `versione_app`           | Versione dell'app                                              |
| `numero_crash`           | Numero crash subiti                                            |
| `latency_media`          | Latency media in ms                                            |
| `bug_rilevati`           | Bug segnalati                                                  |
| `cluster_comportamentale`| Tipo giocatore (Casual, Hardcore, Spender)                     |
| `canale_acquisizione`    | Canale acquisizione (Pubblicità, Referral, Organic)            |
| `campagne_risposta`      | Numero campagne marketing risposte                             |
| `profilo_social_integrato`| 0 = No, 1 = Sì                                                |

---

## 3. Variable Notes
- **eta**: Alcuni valori mancanti per simulare scenari reali.
- **salute_media, attacco_medio, crediti_attuali, spesa_mensile**: Contengono valori mancanti, che verranno imputati con la media.
- **genere, istruzione, classe_personaggio**: Alcuni missing che richiederanno rimozione o imputazione.
- **numero_battaglie, vittorie, sconfitte**: Coerenti, ma non garantita la somma logica (semplificazione).
- **cluster_comportamentale**: Utile per segmentazione utenti.

---

## 4. EDA Plan
- **Analisi univariata**: Distribuzione età, spesa_mensile, soddisfazione, cluster_comportamentale.
- **Analisi bivariata**: Relazione tra spesa_mensile e cluster, livello e classe_personaggio, genere e numero_battaglie.
- **Analisi multivariata**: Heatmap delle correlazioni numeriche.
- **Gestione missing values**: Imputazione media per numerici, rimozione righe per categorici.
- **Creazione feature derivate**: es. rapporto vittorie/sconfitte, engagement ratio.

---

## 5. Techniques Used
- Data Cleaning: Gestione valori mancanti e outlier detection.
- Feature Engineering: Creazione variabili composite.
- Visualizzazioni: Istogrammi, boxplot, heatmap, barplot.
- Analisi per gruppi: Cluster_comportamentale, classe_personaggio, dispositivo.

---

## 6. Insights attesi
- Giocatori **Hardcore** giocano più ore e spendono di più.
- **Mobile vs PC**: differenze in engagement e spesa.
- **Età e spesa**: Fasce giovani spendono meno rispetto agli Spender.

---

## 7. Future Enhancements
- Prevedere **churn** (abbandono) in base al comportamento.
- Prevedere **la soddisfazione** degli utenti.
- Segmentazione utenti per campagne marketing personalizzate.
- Analisi predittiva: modello ML per prevedere spesa mensile.
