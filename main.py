
# Importez les classes nécessaires
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd  # Importez pandas
from preprocessing import preprocessing

app = FastAPI()

# Chargez le modèle à partir du fichier joblib
model = joblib.load('popularity_corner/best_model/modele.pkl')

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
def predict_cinema_entries(inputs: FilmInput):
    # Utiliser la fonction preprocessing pour transformer les données d'entrée
    input_data = preprocessing(inputs.director, inputs.distributor, inputs.duration, inputs.genre, inputs.cast,
                               inputs.nationality, inputs.release_date, inputs.title, inputs.views)

    # Convertir les données prétraitées en DataFrame
    input_df = pd.DataFrame(input_data, index=[0])

    # Faire la prédiction en utilisant le modèle chargé
    prediction = model.predict(input_df)

    # Créer une instance de la classe de sortie PredictionOut avec la prédiction
    output = PredictionOut(box_office_first_week=prediction[0])

    # Retourner la prédiction
    return output