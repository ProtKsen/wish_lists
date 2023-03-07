from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render

from friends.models import Friend, FriendRequest
from userprofile.models import Wish


def all_friends(request):
    all_friends_objects = Friend.objects.filter(user=request.user)
    context = {
        'friends': [object.friend for object in all_friends_objects]
    }
    return render(request, 'all_friends.html', context=context)


def friend_profile(request, id: int):
    wishes = Wish.objects.filter(user_id=id)
    all_types = list(Wish.objects.filter(user_id=id).values('type'))
    set_of_types = set([i['type'] for i in all_types])
    context = {
        'wishes': wishes,
        'set_of_types': set_of_types
    }
    return render(request, 'friend_profile.html', context)


def all_users(request):
    all_users_objects = User.objects.filter(~Q(username=request.user.username))
    users = []
    for object in all_users_objects:
        is_friend = Friend.objects.filter(user=request.user, friend=object).first()
        users.append({'id': object.id, 'name': object.username, 'is_friend': is_friend})

    context = {
        'users': users
    }
    return render(request, 'all_users.html', context)


def send_request(request, id: int):
    friend = User.objects.get(id=id)
    friend_request = FriendRequest(from_user=request.user, to_user=friend, status='pending')
    friend_request.save()
    return redirect('all_users')


def all_friend_requests(request):
    pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    context = {
        'requests': pending_requests
    }
    return render(request, 'all_friend_requests.html', context)


def accept_request(request, id: int):
    friend = User.objects.get(id=id)
    friend_request = FriendRequest.objects.get(to_user=request.user, from_user=friend)
    friend_request.status = 'accepted'
    friend_request.save()

    new_friend = Friend(user=request.user, friend=friend)
    symm_new_friend = Friend(user=friend, friend=request.user)
    new_friend.save()
    symm_new_friend.save()

    return redirect('userprofile')


def reject_request(request, id: int):
    friend = User.objects.get(id=id)
    friend_request = FriendRequest.objects.get(to_user=request.user, from_user=friend)
    friend_request.status = 'rejected'
    friend_request.save()
    return redirect('userprofile')


def delete_friend(request, id):
    friend = User.objects.get(id=id)
    Friend.objects.get(user=friend, friend=request.user).delete()
    Friend.objects.get(user=request.user, friend=friend).delete()
    return redirect('userprofile')
