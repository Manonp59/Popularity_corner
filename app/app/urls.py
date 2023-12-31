from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),
    path('contact/', views.contactpage, name='contact'),
    path('estimations/', views.update_predictions, name="predictions"),
    path('resultats/', views.get_resultats, name="resultats"),
    path('login/', views.user_login, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('about/', views.aboutpage, name='about'),
    #path('dashboard/', views.dashboard, name='dashboard'),
]
