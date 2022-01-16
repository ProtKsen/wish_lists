from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')


def contacts(request):
    return render(request, 'contacts.html')

def about(request):
    return render(request, 'about.html')