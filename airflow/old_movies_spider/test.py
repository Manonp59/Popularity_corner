import unittest
from unittest.mock import patch, MagicMock
from api_meteo import get_weather_forecast

class TestWeatherForecastAPI(unittest.TestCase):

    @patch('api_meteo.requests.get')
    def test_get_weather_forecast(self, mock_get):
        # Données fictives de la réponse de l'API pour le test
        forecast_data = {
            'forecast': [
                {'tmax': 25, 'tmin': 15},  # Jour 1
                {'tmax': 28, 'tmin': 17},  # Jour 2
                # Ajoutez d'autres données de prévision pour les jours suivants...
            ]
        }

        # Créez un objet MagicMock pour simuler la réponse de l'API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = forecast_data

        # Définissez le comportement du mock de la méthode 'get' de requests
        mock_get.return_value = mock_response

        # Appel à la fonction d'appel à l'API avec des paramètres fictifs
        api_key = '6ad50f056c5e7be8c781a3e537b1ee893b4bcccdf972e4baf058540cd85373f1'
        latitude = 48.8566
        longitude = 2.3522
        days_to_retrieve = 5
        result = get_weather_forecast(api_key, latitude, longitude, days_to_retrieve)

        # Vérifiez que la fonction renvoie les données de prévision attendues
        self.assertEqual(result, forecast_data['forecast'][:days_to_retrieve])

if __name__ == '__main__':
    unittest.main()
