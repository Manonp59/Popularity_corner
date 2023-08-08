import os
import pandas as pd
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

application = get_wsgi_application()

#from main.models import Upcoming_movie

def import_data_from_csv(file_path):
    data = pd.read_csv(file_path)
    for _, row in data.iterrows():
        title = row['title']
        release_date = row['release_date']
        estimated_audience = 100  ##### À modifier plus tard avec les données de l'api du modèle

        movie = Upcoming_movie(
            title=title, 
            release_date=release_date, 
            estimated_audience=estimated_audience)
        movie.save()

if __name__ == "__main__":
    csv_file_path = "../incoming_movies_spider/next_week.csv"
    import_data_from_csv(csv_file_path)
