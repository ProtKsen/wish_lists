from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Wish
from django.db.models import Count


def userprofile(request):
    wishdata = Wish.objects.filter(username=request.user)
    all_types = Wish.objects.values('type').annotate(type_count=Count('type')).filter(type_count=1, username=request.user)
    context = {
        'wishdata': wishdata,
        'all_types': all_types
    }
    return render(request, 'user_profile.html', context)


def addwish(request):
    if request.method == "POST":
        wish_data = {}
        for i in request.POST.keys():
            if i in ['title', 'link', 'description', 'username', 'type']:
                wish_data[i] = request.POST.get(i)
        wish_data['username'] = User.objects.get(username=request.user)
        try:
            wish_data['image'] = request.FILES['uploadimage']
        except:
            pass
        wishdata = Wish(**wish_data)
        wishdata.save()
        return redirect('userprofile')
    return render(request, 'add_wish.html')


def delete_wish(request, id):
    wishdata = Wish.objects.get(id=id)
    wishdata.delete()
    return redirect('userprofile')


def edit_wish(request, id):
    if request.method == "POST":
        wishdata = Wish.objects.get(id=id)
        wish_data = {}
        for i in request.POST.keys():
            if i in ['title', 'link', 'description', 'username', 'type']:
                wish_data[i] = request.POST.get(i)
        wish_data['username'] = User.objects.get(username=request.user)
        try:
            wish_data['image'] = request.FILES['uploadimage']
        except:
            pass
        wishdata.save()
        return redirect('userprofile')
    else:
        wishdata = Wish.objects.get(id=id)
        context = {
            'title': wishdata.title,
            'link': wishdata.link,
            'description': wishdata.description,
            'image': wishdata.image,
            'type': wishdata.type
        }
        return render(request, 'edit_wish.html', context)


def wish_details(request, id):
    wishdata = Wish.objects.get(id=id)
    context = {
        'wishdata': wishdata,
    }
    return render(request, 'wish_details.html', context)
