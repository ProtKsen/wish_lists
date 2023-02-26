from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User


def authentication(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(request, username=name, password=password)
        if user:
            login(request, user)
            return redirect('userprofile')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'authentication.html')


def authlogout(request):
    logout(request)
    return redirect('home')


def forget_password(request):
    return render(request, 'forget_password.html')


def authregistration(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=name).exists():
                messages.error(request, 'Пользователь с таким именем уже существует')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Пользователь с таким email уже существует')
            else:
                user = User.objects.create_user(username=name, email=email, password=password)
                user.save()
                login(request, user)
                return redirect('userprofile')
        else:
            messages.error(request, 'Пароли не совпадают')
    return render(request, 'registration.html')
