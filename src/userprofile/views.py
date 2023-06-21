from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from django.utils.datastructures import MultiValueDictKeyError
from PIL import Image, UnidentifiedImageError

from userprofile.forms import WishForm

from .models import Wish

ALLOWED_IMAGE_EXTENSIONS = ["png", "jpg", "jpeg"]


@login_required
@user_passes_test(lambda u: u.is_active, login_url="login")
def userprofile(request):
    wishes = Wish.objects.filter(user=request.user.id)
    types = set([wish.type for wish in wishes])
    context = {"wishes": wishes, "types": types}
    return render(request, "user_profile.html", context)


@login_required
@user_passes_test(lambda u: u.is_active, login_url="login")
def addwish(request):
    if request.method == "POST":
        form = WishForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data

            wish_data = {}
            for key, val in form_data.items():
                if val:
                    wish_data[key] = val

            try:
                file = Image.open(request.FILES["file"])
                if file.format.lower() not in ALLOWED_IMAGE_EXTENSIONS:
                    raise UnidentifiedImageError
                wish_data["image"] = request.FILES["file"]

            except UnidentifiedImageError:
                messages.add_message(request, messages.ERROR, "Неверный формат файла.")
                form = WishForm(initial=wish_data)
                context = {"form": form}
                return render(request, "add_wish.html", context)

            except MultiValueDictKeyError:
                pass

            wish_data["user"] = request.user
            wish = Wish(**wish_data)
            wish.save()
            return redirect("userprofile")

    form = WishForm()
    context = {"form": form}
    return render(request, "add_wish.html", context)


@login_required
def delete_wish(request, id: int):
    wish = Wish.objects.get(id=id)
    image = wish.image
    if image.name != "img/wish_default.jpg":
        image.delete()
    wish.delete()
    return redirect("userprofile")


@login_required
def edit_wish(request, id: int):
    wish = Wish.objects.get(id=id)
    initial_data = {
        "title": wish.title,
        "link": wish.link,
        "description": wish.description,
        "type": wish.type,
        "image": wish.image,
    }
    if request.method == "POST":
        form = WishForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data

            new_wish_data = {}
            for key, val in form_data.items():
                if val:
                    new_wish_data[key] = val

            try:
                file = Image.open(request.FILES["file"])
                if file.format.lower() not in ALLOWED_IMAGE_EXTENSIONS:
                    raise UnidentifiedImageError
                new_wish_data["image"] = request.FILES["file"]

            except UnidentifiedImageError:
                messages.add_message(request, messages.ERROR, "Неверный формат файла.")
                form = WishForm(initial=new_wish_data)
                context = {"form": form}
                return render(request, "edit_wish.html", context)

            new_wish_data["user"] = request.user
            wish = Wish.objects.get(id=id)
            for key, value in new_wish_data.items():
                setattr(wish, key, value)
            wish.save()
            return redirect("userprofile")
    else:
        form = WishForm(initial=initial_data)
        context = {"form": form}
        return render(request, "edit_wish.html", context)


@login_required
def wish_details(request, id: int):
    wish = Wish.objects.get(id=id)
    context = {
        "wish": wish,
    }
    return render(request, "wish_details.html", context)
