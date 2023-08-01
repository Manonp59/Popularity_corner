
# Importez les classes nécessaires
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd  # Importez pandas

app = FastAPI()

# Chargez le modèle à partir du fichier joblib
model = joblib.load('/home/apprenant/DevIA/Popularity_corner/popularity_corner/best_model/modele.pkl')

# Modèle de données pour les entrées au cinéma
class FilmInput(BaseModel):
    director : str 
    distributor : str 
    duration : str 
    genre : str
    cast : str 
    nationality : str 
    release_date : str 
    title : str 
    views : int 
    
class PredictionOut(BaseModel):
    box_office_first_week : float

# Route pour la prédiction
@app.post("/predict/")
def predict_cinema_entries(inputs: CinemaInput):
    # Convertir les données en pandas DataFrame et renommer les colonnes
    result = predict_pipeline()

    # Utiliser le modèle pour faire la prédiction
    prediction = model.predict(data)
    return {"cinema_entries": prediction[0]}