from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv
# Charger les variables d'environnement à partir du fichier .env
load_dotenv()


def get_weather_forecast(api_key, latitude, longitude, days):
    url = f"https://api.meteo-concept.com/api/forecast/daily?token={api_key}&latlng={latitude},{longitude}"
    
    response = requests.get(url)
    if response.status_code == 200:
        forecast_data = response.json()
        return forecast_data['forecast'][:days]
    else:
        print("Erreur lors de la requête API.")
        return None

def calculate_average_temperature(forecast_data, days):
    if len(forecast_data) < days:
        print(f"Les prévisions ne couvrent pas {days} jours.")
        return None

    total_temperature = 0
    for day_forecast in forecast_data[:days]:
        temperature_max = day_forecast['tmax']
        temperature_min = day_forecast['tmin']
        daily_temperature = (temperature_max + temperature_min) / 2
        total_temperature += daily_temperature

    average_temperature = total_temperature / days
    return average_temperature

# Remplacez 'VOTRE_TOKEN' par votre clé d'accès à l'API de Meteo Concept
api_key = os.environ.get('API_KEY_METEO')
cities = [
    {'name': 'Paris', 'lat': 48.8566, 'lon': 2.3522},
    {'name': 'Bordeaux', 'lat': 44.8378, 'lon': -0.5792},
    {'name': 'Lille', 'lat': 50.6292, 'lon': 3.0573},
    {'name': 'Marseille', 'lat': 43.2965, 'lon': 5.3698},
    {'name': 'Lyon', 'lat': 45.7640, 'lon': 4.8357}
]
days_to_retrieve = 14  # Nombre de jours de prévision à récupérer
days_to_calculate_average = 10  # Nombre de jours pour calculer la température moyenne

for city in cities:
    forecast_data = get_weather_forecast(api_key, city['lat'], city['lon'], days_to_retrieve)
    if forecast_data:
        # Traitez ici les données de prévision météorologique pour les jours futurs
        print(f"Prévisions météo pour {city['name']}:")
        print(forecast_data)

        # Calculer la température moyenne pour les 7 premiers jours
        average_temperature_7_days = calculate_average_temperature(forecast_data, days_to_calculate_average)
        if average_temperature_7_days:
            print(f"Température moyenne pour les {days_to_calculate_average} premiers jours : {average_temperature_7_days:.1f}°C")
        else:
            print("Impossible de calculer la température moyenne.")
        print("\n")
    else:
        print(f"Aucune donnée de prévision disponible pour {city['name']}.\n")