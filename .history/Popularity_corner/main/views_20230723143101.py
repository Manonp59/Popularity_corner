from django.shortcuts import render
from main.models import Upcoming_movie

# Create your views here.

def publi


def estimation(request):
    # if not request.user.is_authenticated: #if the user is not authenticated
    #     messages.success(request, "Please login to acces your bookings")
    #     return HttpResponseRedirect(reverse("login")) #redirect to login page
    # else:
        upcoming_movies =  Upcoming_movie.objects.all()
        return render(request, './templates/private/estimations.html',{'upcoming_movies' : upcoming_movies})
    