import hashlib
import random
import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render

from authentication.models import HashSalt


def hashed(in_line: str, salt: str):
    return hashlib.sha256(salt.encode() + in_line.encode()).hexdigest()


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

                user = User.objects.create_user(
                    username=name,
                    email=email,
                    password=password,
                    is_active=False
                )
                user.save()

                email_subject = 'Giftnet. Verification code.'
                verif_password = random.randint(1000, 9999)
                email_body = f'Password is {verif_password}'
                email = EmailMessage(email_subject, email_body, to=[email])
                email.send()

                salt = uuid.uuid4().hex
                hashsolt = HashSalt.objects.create(user=user, salt=salt)
                hashsolt.save()

                hashed_verif_password = hashed(str(verif_password), str(salt))

                return redirect('verification', name, hashed_verif_password)
        else:
            messages.error(request, 'Пароли не совпадают')
    return render(request, 'registration.html')


def authverification(request, name, token):
    if request.method == "POST":

        user = User.objects.get(username=name)
        salt = str(HashSalt.objects.get(user=user).salt)
        password = str(request.POST['password'])
        hashed_password = hashed(password, salt)

        if hashed_password == token:

            user.is_active = True
            user.save()

            email_subject = 'Giftnet. Registration completed successfully.'
            email_body = f'Hello, {user.username}! \n Welcome to Giftnet!'
            email = EmailMessage(email_subject, email_body, to=[user.email])
            email.send()

            login(request, user)

            return redirect('userprofile')
        else:
            messages.error(request, 'Введен неверный код.')

    return render(request, 'verification.html')
