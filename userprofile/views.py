from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Wish


def userprofile(request):
    wishdata = Wish.objects.all()
    context = {
        'wishdata': wishdata,
    }
    return render(request, 'user_profile.html', context)
