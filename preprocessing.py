import pandas as pd 
import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY_BUDGET')
df_stars = pd.read_csv('popularity_corner/stars/stars.csv')
df_distrib = pd.read_csv('popularity_corner/best_model/df_distrib.csv')

def preprocessing(director : str, distributor : str, duration : str, genre : str, cast : str, nationality : str, release_date : str, title : str, views : int):
    release_date = pd.to_datetime(release_date)
    genre = cleaning_genre(genre)
    duration = convert_to_minutes(duration)
    budget = get_budget(get_id(title, api_key),api_key)
    season = get_season(release_date)
    distributor = distributor.replace('/', ',')
    stars_actors = get_stars_cast(cast)
    stars_producers_director = get_stars_producers_director(director)
    distributor_avg_frequency = get_stars_distributor(distributor)
    nationality = nationality
    views = views
    
    data = {
        'duration': [duration],
        'nationality': [nationality],
        'views': [views],
        'genre': [genre],
        'budget': [budget],
        'season': [season],
        'stars_actors': [stars_actors],
        'stars_producers_director': [stars_producers_director],
        'distributor_avg_frequency': [distributor_avg_frequency]
    }
    df = pd.DataFrame(data)

    # Appliquer l'encodage one hot pour le genre
    df = one_hot_encode_genre(df)

    # Convertir le DataFrame en JSON
    output_json = df.to_dict(orient='records')[0]

    return output_json
    

def cleaning_genre(genres_list):
    genres_list = genres_list.lower().split(',')
    genres_list = [genre.strip() for genre in genres_list]
    if 'Drama' in genres_list:
        genres_list = [genre.replace('Drama', 'Drame') for genre in genres_list]
    return ', '.join(genres_list)

def one_hot_encode_genre(df):
    # Liste de tous les genres possibles
    all_genres = ['action', 'animation', 'arts martiaux', 'aventure', 'biopic', 'bollywood', 'comédie', 'comédie dramatique', 'comédie musicale', 'divers', 'drame', 'epouvante-horreur', 'erotique', 'espionnage', 'expérimental', 'famille', 'fantastique', 'guerre', 'historique', 'judiciaire', 'musical', 'policier', 'péplum', 'romance', 'science fiction', 'sport event', 'thriller', 'western']

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


def get_season(release_date):
    month = release_date.month
    if month >=3 and month <= 5:
        return "Spring"
    elif month >=6 and month <= 8:
        return "Summer"
    elif month >=9 and month <= 11:
        return "Autumn"
    else : 
        return "Winter"
    
def get_stars_cast(cast):
    stars = df_stars['name'].to_list()
    count = 0
    for actor in cast:
        if actor in stars:
            count += 1
    return count

def get_stars_cast(cast):
    stars = df_stars['name'].to_list()
    cast = [actor.strip() for actor in cast.split(',')]
    count = 0
    for actor in cast:
        if actor in stars:
            count += 1
    return count

def get_stars_producers_director(directors):
    stars = df_stars['name'].to_list()
    directors = [director.strip() for director in directors.split(',')]
    count = 0
    for director in directors:
        if director in stars:
            count += 1
    return count

def get_stars_distributor(distributor):
    # Séparer les distributeurs en une liste
    distributors_list = [d.strip() for d in distributor.split(',')]

    # Vérifier si la variable distributors est une liste
    if len(distributors_list) > 1:
        # Initialiser une liste pour stocker les fréquences d'apparition
        frequencies = []

        # Parcourir les distributeurs dans la liste
        for distributor in distributors_list:
            # Rechercher la fréquence d'apparition du distributeur
            frequency = df_distrib[df_distrib['distributor'] == distributor]['frequency'].values

            # Si le distributeur est trouvé dans le DataFrame, ajouter sa fréquence à la liste
            if len(frequency) > 0:
                frequencies.append(frequency[0])

        # Si au moins un distributeur est trouvé, retourner la fréquence moyenne des distributeurs trouvés
        if len(frequencies) > 0:
            return sum(frequencies) / len(frequencies)
        else:
            # Sinon, retourner la fréquence moyenne de tous les distributeurs
            return df_distrib['frequency'].mean()

    else:
        # Rechercher la fréquence d'apparition du distributeur
        frequency = df_distrib[df_distrib['distributor'] == distributor]['frequency'].values

        # Si le distributeur n'est pas trouvé dans le DataFrame, retourner la fréquence moyenne
        if len(frequency) == 0:
            return df_distrib['frequency'].mean()

        # Sinon, retourner la fréquence d'apparition
        return frequency[0]