from django.shortcuts import render
from django.http import HttpResponse


def authentication(request):
    return render(request, 'authentication.html')