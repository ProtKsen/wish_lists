from django.urls import path

from views import views

urlpatterns = [
    path('', views.authentication, name='authentication'),
    path('registration/', views.authregistration, name='registration'),
    path('verification/<name>/<token>/', views.authverification, name='verification'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password/verification/<name>/<token>/', views.reset_pass_verification, name='reset_pass_verification'),
    path('change_password/<name>/', views.change_password, name='change_password'),
    path('logout/', views.authlogout, name='logout'),
]
