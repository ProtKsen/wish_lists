from django.shortcuts import render
from friends.models import Friend
from userprofile.models import Wish


def all_friends(request):
    all_friends_objects = Friend.objects.filter(user=request.user)
    context = {
        'friends': [object.friend for object in all_friends_objects]
    }
    return render(request, 'all_friends.html', context=context)


def friend_profile(request, id):
    wishes = Wish.objects.filter(user_id=id)
    all_types = list(Wish.objects.filter(user_id=id).values('type'))
    set_of_types = set([i['type'] for i in all_types])
    context = {
        'wishes': wishes,
        'set_of_types': set_of_types
    }
    return render(request, 'friend_profile.html', context)
