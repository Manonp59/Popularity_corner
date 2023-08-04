from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm
from django.contrib import messages
import requests
from main.models import Upcoming_movie
from dotenv import load_dotenv
import os
from django import template
from datetime import datetime

register = template.Library()

load_dotenv()
api_key = os.getenv('API_KEY_BUDGET')

    

def get_prediction(movie):
    url = 'http://20.199.59.131:80/predict'
    data = {
        'director': movie.director,
        'distributor': movie.distributor,
        'duration': movie.duration,
        'genre': movie.genres,
        'cast': movie.cast,
        'nationality': movie.nationality,
        'release_date': movie.release_date,
        'title': movie.title,
        'views': movie.views
    }
    response = requests.post(url, json=data)
    response.raise_for_status()  # Lève une exception si la requête a échoué
    return response.json()['box_office_first_week']  # Remplacez par le bon chemin pour obtenir la prédiction dans la réponse
def update_predictions(request):
    today = datetime.today()
    movies = Upcoming_movie.objects.filter(release_date__gt=today)
    for movie in movies:
        movie.prediction = get_prediction(movie)
        movie.prediction_cinema = prediction_cinema(movie.prediction)
        movie.save()

    return render(request, 'private/estimations.html', {'movies': movies})

def prediction_cinema(prediction):
    prediction_cinema = prediction/2000
    return prediction_cinema



def homepage(request):
    images = ['media/1.jpg', 'media/2.jpg', 'media/3.jpg', 
              'media/4.jpg', 'media/5.jpg', 'media/6.jpg', 
              'media/7.png', 'media/8.webp', 'media/9.webp', 
              'media/10.webp', 'media/11.webp', 'media/12.webp']
    return render(request, "public/home.html", {"images" : images})
    
def contactpage(request):
        return render(request, "public/contact.html")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, "🍿 - Votre compte a bien été créé.")
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'public/register.html', {"form" : form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect('dashboard')
            else:
                messages.success(request, f"Bienvenu {username} - Vous êtes connecté !")
                return redirect('home')
        else:
            messages.error(request, "Identifiant ou mot de passe incorrect, veuillez réessayer.")
            return redirect('login')

    else:
        return render(request, 'public/login.html') 

def logout_user(request):
    logout(request)
    messages.success(request, "Succesfully Logged out !")
    return redirect('home')