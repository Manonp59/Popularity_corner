# Other imports
import requests
import os

# Django imports
from django import template
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from main.models import Upcoming_movie, Last_week_movie

# Imports from useful libraries
from dotenv import load_dotenv
from datetime import datetime

register = template.Library()

load_dotenv()
api_key = os.getenv('API_KEY_BUDGET')

    

def get_prediction(movie):
    """"
    Sends a POST request to the prediction API with the given movie data and returns the predicted box office for the first week.

    Args:
        movie (Movie): The movie object containing the information to be sent to the API.
        
    Returns:
        float: The predicted box office for the first week.

    Raises:
        HTTPError: If the request to the API fails.
    """
    url = 'http://20.19.17.194:80/predict'
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
    """
    Update the predictions for upcoming movies.

    This function retrieves all upcoming movies whose release date is after today's date
    and updates their prediction and prediction cinema fields based on the movie's data.
    The updated movies are then saved to the database.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered HTML page displaying the updated estimations with the list of movies.
    """
    movies = Upcoming_movie.objects.all()
    for movie in movies:
        print(movie.title)
        movie.prediction = get_prediction(movie)
        movie.prediction_cinema = prediction_cinema(movie.prediction)
        movie.save()

    return render(request, 'private/estimations.html', {'movies': movies})

def prediction_cinema(prediction):
    """
    Calculate the predicted cinema attendance based on the given prediction.

    Parameters:
        prediction (int): The predicted attendance for a cinema.

    Returns:
        float: The calculated predicted cinema attendance.
    """
    prediction_cinema = prediction/2000
    return prediction_cinema

@login_required
def get_resultats(request):
    resultats = Last_week_movie.objects.all()
    return render(request, 'private/resultats.html',{"resultats": resultats})


def homepage(request):
    """
    This function handles the homepage view.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered response for the homepage view.
    """
    images = ['media/1.jpg', 'media/2.jpg', 'media/3.jpg', 
              'media/4.jpg', 'media/5.jpg', 'media/6.jpg', 
              'media/7.png', 'media/8.webp', 'media/9.webp', 
              'media/10.webp', 'media/11.webp', 'media/12.webp']
    return render(request, "public/home.html", {"images": images})
    
def contactpage(request):
        return render(request, "public/contact.html")


def register(request):
    """
    Register function to handle user registration.
    
    Args:
        request (HttpRequest): The HTTP request object.
        
    Returns:
        HttpResponse: The HTTP response object containing the rendered template.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "🍿 - Votre compte a bien été créé.")
            return redirect('home')  # Redirect directly to home
    else:
        form = CustomUserCreationForm()

    return render(request, 'public/register.html', {"form": form})

def user_login(request):
    """
    Logs in a user based on the provided request.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.

    Raises:
        None
    """
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
    """
    Logs out the user and redirects them to the home page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: The redirected response to the home page.
    """
    logout(request)
    messages.success(request, "Succesfully Logged out !")
    return redirect('home')