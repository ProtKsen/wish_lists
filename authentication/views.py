from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def authentication(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'authentication.html')


def authlogout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из аккаунта')
    return redirect('authentication')


def forget_password(request):
    return render(request, 'forget_password.html')


def registration(request):
    return render(request, 'registration.html')
