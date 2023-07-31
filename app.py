# Importez les classes nécessaires
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd  # Importez pandas

app = FastAPI()

# Chargez le modèle à partir du fichier joblib
model = joblib.load('votre_modele.pkl')

# Modèle de données pour les entrées au cinéma
class CinemaInput(BaseModel):
    duration: int
    nationality: str
    views: float
    budget: float
    season: str
    is_holiday: bool
    proportion_stars_actors: int
    proportion_stars_producers: int
    proportion_stars_director: int
    distributor_avg_frequency: float
    genre_action: int
    genre_animation: int
    genre_arts_martiaux: int  # Renommé 'genre_arts_martiaux'
    genre_aventure: int
    genre_biopic: int
    genre_bollywood: int
    genre_comédie: int
    genre_comédie_dramatique: int  # Renommé 'genre_comédie_dramatique'
    genre_comédie_musicale: int  # Renommé 'genre_comédie_musicale'
    genre_divers: int
    genre_drame: int
    genre_epouvante_horreur: int  # Renommé 'genre_epouvante-horreur'
    genre_erotique: int
    genre_espionnage: int
    genre_expérimental: int
    genre_famille: int
    genre_fantastique: int
    genre_guerre: int
    genre_historique: int
    genre_judiciaire: int
    genre_musical: int
    genre_policier: int
    genre_péplum: int
    genre_romance: int
    genre_science_fiction: int  # Renommé 'genre_science fiction'
    genre_sport_event: int  # Renommé 'genre_sport event'
    genre_thriller: int
    genre_western: int

# Route pour la prédiction
@app.post("/predict/")
def predict_cinema_entries(inputs: CinemaInput):
    # Convertir les données en pandas DataFrame et renommer les colonnes
    data = pd.DataFrame([inputs.dict()])
    data = data.rename(columns={
        'genre_arts_martiaux': 'genre_arts martiaux',
        'genre_comédie_dramatique': 'genre_comédie dramatique',
        'genre_comédie_musicale': 'genre_comédie musicale',
        'genre_epouvante_horreur': 'genre_epouvante-horreur',
        'genre_science_fiction': 'genre_science fiction',
        'genre_sport_event': 'genre_sport event'
    })

    # Utiliser le modèle pour faire la prédiction
    prediction = model.predict(data)
    return {"cinema_entries": prediction[0]}
