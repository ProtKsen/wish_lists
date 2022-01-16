from django.contrib import admin
from django.urls import path
from index import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about')
]