from django.contrib import admin
from django.urls import path
from authentication import views

urlpatterns = [
    path('', views.authentication, name='authentication'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('registration/', views.registration, name='registration'),
    ]