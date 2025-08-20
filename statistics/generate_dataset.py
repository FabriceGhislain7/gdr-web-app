import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()

# Numero di righe del dataset
N = 50000

# -----------------------
# Funzioni di supporto
# -----------------------
def random_choice_weighted(options, weights):
    """
    Restituisce un valore casuale da una lista di opzioni, pesato in base ai pesi forniti.

    Args:
        options (list): Lista di possibili valori da selezionare.
        weights (list): Lista di pesi (probabilità) corrispondenti a ciascuna opzione. 
                        La somma dei pesi deve essere 1.

    Returns:
        object: Un valore scelto casualmente dalla lista 'options' secondo la distribuzione 'weights'.
    """
    return np.random.choice(options, p=weights)


def generate_class():
    """Genera una classe di personaggio casuale."""
    return random_choice_weighted(['Mago', 'Guerriero', 'Ladro'], [0.4, 0.4, 0.2])


def generate_device():
    """Genera il tipo di dispositivo usato dal giocatore."""
    return random_choice_weighted(['PC', 'Mobile', 'Tablet'], [0.5, 0.4, 0.1])


def generate_cluster():
    """Genera il cluster comportamentale del giocatore."""
    return random_choice_weighted(['Casual', 'Hardcore', 'Spender'], [0.6, 0.3, 0.1])


def generate_acquisition():
    """Genera il canale di acquisizione del giocatore."""
    return random_choice_weighted(['Pubblicità', 'Referral', 'Organic'], [0.5, 0.2, 0.3])


def generate_ora_punta():
    """
    Genera l'ora del giorno (0-23) in cui il giocatore è più attivo.
    Distribuzione simulata in base alle ore comuni di picco.
    """
    weights = [5,3,2,2,1,1,2,5,8,10,12,10,8,7,6,4,4,4,3,2,2,1,1,1]  # Frequenze
    return np.random.choice(list(range(24)), p=np.array(weights)/sum(weights))


def generate_items():
    """
    Genera una lista di oggetti casuali posseduti/acquistati dal giocatore.
    """
    items = ['Pozione', 'Medaglione', 'Bomba', 'Spada', 'Scudo']
    return ','.join(random.choices(items, k=random.randint(1, 3)))


# -----------------------
# Generazione dataset
# -----------------------
data = {
    'player_id': [i+1 for i in range(N)],
    'nome': [fake.first_name() for _ in range(N)],
    'eta': np.random.randint(13, 70, N),
    'genere': np.random.choice(['M', 'F'], N, p=[0.48, 0.52]),
    'paese': [fake.country() for _ in range(N)],
    'città': [fake.city() for _ in range(N)],
    'mestiere': [fake.job() for _ in range(N)],
    'istruzione': np.random.choice(['Scuola Media', 'Superiore', 'Università', 'Post-Laurea'], N, p=[0.2,0.4,0.3,0.1]),
    'soddisfazione': np.random.randint(1,11,N),
    'classe_personaggio': [generate_class() for _ in range(N)],
    'livello': np.random.randint(1,101,N),
    'salute_media': np.random.randint(20,101,N),
    'attacco_medio': np.random.randint(5,51,N),
    'destrezza': np.random.randint(1,21,N),
    'oggetti_usati': [generate_items() for _ in range(N)],
    'numero_battaglie': np.random.randint(1,501,N),
    'numero_vittorie': np.random.randint(0,501,N),
    'numero_sconfitte': np.random.randint(0,501,N),
    'tempo_totale_giocato': np.random.randint(10,20000,N),
    'crediti_attuali': np.random.randint(0,5000,N),
    'spesa_mensile': np.random.lognormal(mean=2.0, sigma=1.0, size=N).astype(int),
    'numero_acquisti': np.random.randint(0,100,N),
    'tipo_acquisti': [generate_items() for _ in range(N)],
    'abbonamento_attivo': np.random.choice([0,1], N, p=[0.7,0.3]),
    'rimborso_totale': np.random.randint(0,1000,N),
    'giorni_attivi': np.random.randint(1,365,N),
    'sessioni_giornaliere_medie': np.round(np.random.uniform(0.5,5,N),1),
    'durata_media_sessione': np.random.randint(5,180,N),
    'ora_punta_login': [generate_ora_punta() for _ in range(N)],
    'giorno_settimana_attivo': np.random.choice(['Lun','Mar','Mer','Gio','Ven','Sab','Dom'], N),
    'pausa_media_tra_sessioni': np.round(np.random.uniform(1,72,N),1),
    'tipo_dispositivo': [generate_device() for _ in range(N)],
    'versione_app': np.random.choice(['1.0','1.1','1.2','2.0'], N, p=[0.2,0.3,0.3,0.2]),
    'numero_crash': np.random.randint(0,10,N),
    'latency_media': np.random.randint(10,300,N),
    'bug_rilevati': np.random.randint(0,10,N),
    'cluster_comportamentale': [generate_cluster() for _ in range(N)],
    'canale_acquisizione': [generate_acquisition() for _ in range(N)],
    'campagne_risposta': np.random.randint(0,20,N),
    'profilo_social_integrato': np.random.choice([0,1], N, p=[0.7,0.3])
}

# Creazione DataFrame
df = pd.DataFrame(data)

# Salvataggio CSV
df.to_csv('big_dataset_gioco.csv', index=False)
print("✅ Dataset generato e salvato come 'big_dataset_gioco.csv' con", N, "righe.")
