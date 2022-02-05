from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.userprofile, name='userprofile'),
    path('add_wish/', views.addwish, name='addwish'),
    path('wish_details/<int:id>/', views.wish_details, name='wishdetails'),
    path('delete_wish/<int:id>/', views.delete_wish, name='deletewish'),
    path('edit_wish/<int:id>/', views.edit_wish, name='editwish'),
    ]