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


def addwish(request):
    if request.method == "POST":
        title = request.POST.get('title')
        link = request.POST.get('link')
        description = request.POST.get('description')
        wishdata = Wish(title=title, link=link, description=description)
        wishdata.save()
        return redirect('userprofile')
    return render(request, 'add_wish.html')


def wish_details(request, id):
    wishdata = Wish.objects.get(id=id)
    context = {
        'wishdata': wishdata,
    }
    return render(request, 'wish_details.html', context)
