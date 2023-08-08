from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from main.models import Upcoming_movie

def estimation(request):
    if not request.user.is_authenticated: #if the user is not authenticated
        messages.success(request, "Please login to acces your bookings")
        return HttpResponseRedirect(reverse("login")) #redirect to login page
    else:
        upcoming_movies =  Upcoming_movie.objects.all()
        return render(request, 'estimations.html',{'upcoming_movies' : upcoming_movies, "user" : request.user})
    
def homepage(request):
        return render(request, "")


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, "Account created, you're now logged in")
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'authentication/register.html', {
        "form" : form,
        })

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect('planning')
            else:
                messages.success(request, "You're now logged in")
                return redirect('home')
        else:
            messages.success(request, "Could not log you in, verify your username/password")
            return redirect('login')

    else:
        return render(request, 'authentication/login.html') 

def logout_user(request):
    logout(request)
    messages.success(request, "Succesfully Logged out !")
    return redirect('home')
