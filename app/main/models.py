from django.db import models

class Upcoming_movie(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.CharField(max_length=200)
    genres = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    cast = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    views = models.IntegerField()
    nationality = models.CharField(max_length=100)
    distributor = models.CharField(max_length=200)
    prediction = models.FloatField(null=True, blank=True)
    image_url = models.CharField(max_length=200)
    prediction_cinema = models.FloatField(null=True,blank=True)
    
    class Meta:
        db_table = 'main_upcoming_movies'
        
class Last_week_movie(models.Model):
    title = models.CharField(max_length=200)
    week = models.CharField(max_length=200)
    entrance = models.IntegerField()
    country = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'main_last_week_movies'
