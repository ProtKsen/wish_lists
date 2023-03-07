from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from userprofile.forms import WishForm

from .models import Wish


@login_required
def userprofile(request):
    wishes = Wish.objects.filter(user=request.user.id)
    all_types = list(Wish.objects.filter(user=request.user.id).values('type'))
    set_of_types = set([i['type'] for i in all_types])
    context = {
        'wishes': wishes,
        'set_of_types': set_of_types
    }
    return render(request, 'user_profile.html', context)


@login_required
def addwish(request):
    if request.method == "POST":
        form = WishForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            wish_data = {}
            for key, val in form_data.items():
                if val:
                    wish_data[key] = val
            if 'image' in request.FILES:
                wish_data['image'] = request.FILES['image']
            wish_data['user'] = request.user
            wish = Wish(**wish_data)
            wish.save()
            return redirect('userprofile')
    form = WishForm()
    context = {
        'form': form
    }
    return render(request, 'add_wish.html', context)


@login_required
def delete_wish(request, id: int):
    wish = Wish.objects.get(id=id)
    wish.image.delete()
    wish.delete()
    return redirect('userprofile')


@login_required
def edit_wish(request, id: int):
    wish = Wish.objects.get(id=id)
    initial_data = {
        'title': wish.title,
        'link': wish.link,
        'description': wish.description,
        'type': wish.type,
        'image': wish.image,
    }
    if request.method == "POST":
        form = WishForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            new_wish_data = {}
            for key, val in form_data.items():
                if val:
                    new_wish_data[key] = val
            if 'image' in request.FILES:
                new_wish_data['image'] = request.FILES['image']
            new_wish_data['user'] = request.user
            wish = Wish.objects.get(id=id)
            for key, value in new_wish_data.items():
                setattr(wish, key, value)
            wish.save()
            return redirect('userprofile')
    else:
        form = WishForm(initial=initial_data)
        context = {
            'form': form
        }
        return render(request, 'edit_wish.html', context)


@login_required
def wish_details(request, id: int):
    wish = Wish.objects.get(id=id)
    context = {
        'wish': wish,
    }
    return render(request, 'wish_details.html', context)
