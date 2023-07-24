from django.db import models

class Upcoming_movie(models.Model):
    title = models.fields.CharField(max_length =50)
    release_date = models.fields.DateField(auto_now=False, auto_now_add=False)
    estimated_audience = models.fields.IntegerField()