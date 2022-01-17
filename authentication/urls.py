from django.contrib import admin
from django.urls import path
from authentication import views

urlpatterns = [
    path('', views.authentication, name='authentication'),

    ]