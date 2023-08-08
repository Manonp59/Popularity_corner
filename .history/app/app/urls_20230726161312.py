from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),
    path('estimations/', views.estimation, name="estimations"),
    path('login/', views.login_, name='login'),
    path('logout_user/', views.logout, name='logout'),
    path('register/', views.register, name='register'),

]
