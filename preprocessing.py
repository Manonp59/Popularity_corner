import pandas as pd 
import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY_BUDGET')

def preprocessing(director : str, distributor : str, duration : str, genre : str, cast : str, nationality : str, release_date : str, title : str, views : int):
    release_date = pd.to_datetime(release_date)
    genre = cleaning_genre(genre)
    duration = convert_to_minutes(duration)
    budget = get_budget(get_id(title, api_key),api_key)
    
    data = {
        'director': [director],
        'distributor': [distributor],
        'duration': [duration],
        'genre': [genre],
        'cast': [cast],
        'nationality': [nationality],
        'release_date': [release_date],
        'title': [title],
        'views': [views]
    }
    df = pd.DataFrame(data)

    # Appliquer l'encodage one hot pour le genre
    df = one_hot_encode_genre(df)

    # Convertir le DataFrame en JSON
    output_json = df.to_dict(orient='records')[0]

    return output_json
    

def cleaning_genre(genres_list):
    genres_list = genres_list.split(',')
    genres_list = [genre.strip() for genre in genres_list]
    if 'Drama' in genres_list:
        genres_list = [genre.replace('Drama', 'Drame') for genre in genres_list]
    return ', '.join(genres_list)

def one_hot_encode_genre(df):
    # Liste de tous les genres possibles
    all_genres = ['Action', 'Animation', 'Arts martiaux', 'Aventure', 'Biopic',
                  'Bollywood', 'Comédie', 'Comédie dramatique', 'Comédie musicale',
                  'Divers', 'Drame', 'Epouvante-horreur', 'Erotique', 'Espionnage',
                  'Expérimental', 'Famille', 'Fantastique', 'Guerre', 'Historique',
                  'Judiciaire', 'Musical', 'Policier', 'Péplum', 'Romance',
                  'Science fiction', 'Sport event', 'Thriller', 'Western']

    # Encodage du genre
    genre_encoding = df['genre'].str.get_dummies(sep=',')
    genre_encoding.columns = ['genre_' + col for col in genre_encoding.columns]

    # Ajouter les genres manquants dans chaque ligne
    for genre in all_genres:
        df['genre_' + genre] = df['genre'].apply(lambda x: 1 if genre.lower() in x else 0)

    # Supprimer la colonne "genre" d'origine
    df.drop(columns=['genre'], inplace=True)

    return df

def convert_to_minutes(duration):
    if 'h' in duration and 'min' in duration:
        time_parts = duration.split('h')
        hours = int(time_parts[0])
        minutes = int(time_parts[1].replace('min', '').strip())
    elif 'h' in duration:
        hours = int(duration.replace('h', '').strip())
        minutes = 0
    else:
        raise ValueError("Format de temps invalide. Utilisez '1h' ou '1h 20min'.")

    duration = hours * 60 + minutes

    return duration



def get_id(name, api_key):
    base_url = 'https://api.themoviedb.org/3/search/movie'
    url = f'{base_url}?api_key={api_key}&query={name}'
    response = requests.get(url)
    if response.status_code == 200:
        search_results = response.json()
        if search_results['total_results'] > 0:
            # Prendre le premier résultat de la liste (vous pouvez afficher tous les résultats si nécessaire)
            first_result = search_results['results'][0]
            movie_id = first_result['id']
            return movie_id
        else:
            return f"Aucun résultat trouvé pour '{name}'."
    else:
        return "Erreur lors de la requête API 1 ."

def get_budget(movie_id, api_key):
    base_url = 'https://api.themoviedb.org/3/movie/'
    url = f'{base_url}{movie_id}?api_key={api_key}'

    # Effectuer la requête
    response = requests.get(url)

    # Analyser la réponse JSON
    if response.status_code == 200:
        movie_data = response.json()
        budget = movie_data.get('budget')
        return budget
    else:
        return "Erreur lors de la requête API 2."


