import hashlib
import random
import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

import authentication.message_text
from authentication.forms import (
    EmailForm,
    LoginForm,
    NewPasswordForm,
    RegistrationForm,
    VerificationCodeForm,
)
from authentication.models import HashSalt


def hashed(in_line: str, salt: str) -> str:
    # hash string using "salt"
    return hashlib.sha256(salt.encode() + in_line.encode()).hexdigest()


@require_http_methods(["GET", "POST"])
def authlogin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            username = data["username"]
            password = data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("userprofile")
            else:
                messages.error(request, authentication.message_text.not_valid_username_or_password)
        else:
            messages.error(request, authentication.message_text.not_valid_data)

    form = LoginForm()
    context = {"form": form}
    return render(request, "login.html", context)


@require_http_methods(["GET"])
@login_required
def authlogout(request):
    logout(request)
    return redirect("home")


@require_http_methods(["GET", "POST"])
@user_passes_test(lambda u: u.is_anonymous, login_url="home")
def authregistration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data["username"]
            email = data["email"]
            password = data["password"]

            if User.objects.filter(username=username).exists():
                messages.error(request, authentication.message_text.username_is_used)
            elif User.objects.filter(email=email).exists():
                messages.error(request, authentication.message_text.email_is_used)
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password, is_active=False
                )
                user.save()

                email_subject = "Giftnet. Verification code."
                verification_code = random.randint(1000, 9999)
                email_body = f"Verification code is {verification_code}"
                email = EmailMessage(email_subject, email_body, to=[email])
                email.send()

                salt = uuid.uuid4().hex
                hashsolt = HashSalt.objects.create(user=user, salt=salt)
                hashsolt.save()

                hashed_verification_code = hashed(str(verification_code), str(salt))

                return redirect("verification", username, hashed_verification_code)
    else:
        form = RegistrationForm()
    context = {"form": form}
    return render(request, "registration.html", context)


@require_http_methods(["GET", "POST"])
@user_passes_test(lambda u: u.is_anonymous, login_url="home")
def authverification(request, name: str, token: str):
    try:
        user = User.objects.get(username=name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(request.method)

    if user.is_active:
        return HttpResponseNotFound(request.method)

    if request.method == "POST":
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            salt = HashSalt.objects.get(user=user).salt
            verification_code = data["verification_code"]
            hashed_verification_code = hashed(str(verification_code), str(salt))

            if hashed_verification_code == token:
                user.is_active = True
                user.save()

                email_subject = "Giftnet. Registration completed successfully."
                email_body = f"Hello, {user.username}! \n Welcome to Giftnet!"
                email = EmailMessage(email_subject, email_body, to=[user.email])
                email.send()

                login(request, user)

                return redirect("userprofile")
            else:
                messages.error(request, authentication.message_text.not_valid_verification_code)
        else:
            messages.error(request, authentication.message_text.not_valid_verification_code)

    form = VerificationCodeForm()
    context = {"form": form}
    return render(request, "verification.html", context)


@require_http_methods(["GET", "POST"])
def reset_password(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data["email"]
            if not User.objects.filter(email=email).exists():
                messages.error(request, authentication.message_text.email_is_not_used)
            else:
                user = User.objects.get(email=email)
                email_subject = "Giftnet. Verification code."
                verification_code = random.randint(1000, 9999)
                email_body = f"Password is {verification_code}"
                email = EmailMessage(email_subject, email_body, to=[email])
                email.send()

                salt = HashSalt.objects.get(user=user)

                hashed_verification_code = hashed(str(verification_code), str(salt))

                return redirect("reset_pass_verification", user.username, hashed_verification_code)
    form = EmailForm()
    context = {"form": form}
    return render(request, "reset_password.html", context)


@require_http_methods(["GET", "POST"])
def reset_pass_verification(request, name: str, token: str):
    try:
        user = User.objects.get(username=name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(request.method)

    if request.method == "POST":
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            password = data["password"]
            confirm_password = data["confirm_password"]
            verification_code = data["verification_code"]

            if password == confirm_password:
                salt = HashSalt.objects.get(user=user)
                if hashed(str(verification_code), str(salt)) == token:
                    user.set_password(password)
                    user.save()
                    email_subject = "Giftnet. Password was changed."
                    email_body = (
                        f"Hello, {user.username}! \n Your password was successfully changed."
                    )
                    email = EmailMessage(email_subject, email_body, to=[user.email])
                    email.send()
                    return redirect("login")
                messages.error(request, authentication.message_text.not_valid_verification_code)
            else:
                messages.error(
                    request, authentication.message_text.not_equals_password_confirm_password
                )

        else:
            messages.error(request, authentication.message_text.not_valid_verification_code)

    form = VerificationCodeForm()
    context = {"form": form}
    return render(request, "reset_pass_verification.html", context)
