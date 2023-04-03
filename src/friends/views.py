from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect, render

from friends.models import Friend, FriendRequest
from userprofile.models import Wish


def be_friends_required(func):
    def wrapper(request, *args, **kwargs):
        friend = User.objects.get(id=kwargs['id'])
        all_friends_objects = Friend.objects.filter(user=request.user)
        all_friends_lst = [object.friend for object in all_friends_objects]
        if friend not in all_friends_lst:
            raise PermissionDenied
        return func(request, *args, **kwargs)
    return wrapper


def not_be_friends_required(func):
    def wrapper(request, *args, **kwargs):
        friend = User.objects.get(id=kwargs['id'])
        all_friends_objects = Friend.objects.filter(user=request.user)
        all_friends_lst = [object.friend for object in all_friends_objects]
        if friend in all_friends_lst:
            raise PermissionDenied
        return func(request, *args, **kwargs)
    return wrapper


def no_pending_requests_required(func):
    def wrapper(request, *args, **kwargs):
        friend = User.objects.get(id=kwargs['id'])
        pending_request_from_user = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=friend,
            status=FriendRequest.RequestStatus.PENDING
        )
        pending_request_to_user = FriendRequest.objects.filter(
            from_user=friend,
            to_user=request.user,
            status=FriendRequest.RequestStatus.PENDING
        )
        if pending_request_from_user or pending_request_to_user:
            raise PermissionDenied
        return func(request, *args, **kwargs)
    return wrapper


@login_required
def all_friends(request):
    all_friends_objects = Friend.objects.filter(user=request.user)
    context = {
        'friends': [object.friend for object in all_friends_objects]
    }
    return render(request, 'all_friends.html', context=context)


@login_required
@be_friends_required
def friend_profile(request, id: int):
    wishes = Wish.objects.filter(user_id=id)
    all_types = list(wishes.values('type'))
    set_of_types = set([i['type'] for i in all_types])
    context = {
        'wishes': wishes,
        'set_of_types': set_of_types
    }
    return render(request, 'friend_profile.html', context)


@login_required
def all_users(request):
    all_users_objects = User.objects.exclude(
        Q(username=request.user.username) | Q(is_active=False)
    )
    users = []
    for object in all_users_objects:
        is_friend = Friend.objects.filter(user=request.user, friend=object).first()
        status = 'None'
        if not is_friend:
            request_from_user = FriendRequest.objects.filter(
                from_user=request.user,
                to_user=object,
                status=FriendRequest.RequestStatus.PENDING
            )
            request_to_user = FriendRequest.objects.filter(
                from_user=object,
                to_user=request.user,
                status=FriendRequest.RequestStatus.PENDING
            )
            if request_from_user:
                status = 'request_sent'
            elif request_to_user:
                status = 'request_received'

        users.append(
            {
                'id': object.id,
                'name': object.username,
                'is_friend': is_friend,
                'status': status
            }
        )

    context = {'users': users}
    return render(request, 'all_users.html', context)


@login_required
@not_be_friends_required
@no_pending_requests_required
def send_request(request, id: int):
    friend = User.objects.get(id=id)
    friend_request = FriendRequest(
        from_user=request.user,
        to_user=friend,
        status=FriendRequest.RequestStatus.PENDING
    )
    friend_request.save()
    return redirect('all_users')


@login_required
def all_friend_requests(request):
    pending_requests = FriendRequest.objects.filter(
        to_user=request.user,
        status=FriendRequest.RequestStatus.PENDING
    )
    context = {'requests': pending_requests}
    return render(request, 'all_friend_requests.html', context)


@login_required
@not_be_friends_required
def accept_request(request, id: int):
    friend = User.objects.get(id=id)
    friend_request = FriendRequest.objects.get(
        to_user=request.user,
        from_user=friend,
        status=FriendRequest.RequestStatus.PENDING
    )
    friend_request.status = FriendRequest.RequestStatus.ACCEPTED
    friend_request.save()

    new_friend = Friend(user=request.user, friend=friend)
    symm_new_friend = Friend(user=friend, friend=request.user)
    new_friend.save()
    symm_new_friend.save()

    return redirect('userprofile')


@login_required
@not_be_friends_required
def reject_request(request, id: int):
    friend = User.objects.get(id=id)
    friend_request = FriendRequest.objects.get(
        to_user=request.user,
        from_user=friend,
        status=FriendRequest.RequestStatus.PENDING
    )
    friend_request.status = FriendRequest.RequestStatus.REJECTED
    friend_request.save()
    return redirect('userprofile')


@login_required
@be_friends_required
def delete_friend(request, id):
    friend = User.objects.get(id=id)
    Friend.objects.get(user=friend, friend=request.user).delete()
    Friend.objects.get(user=request.user, friend=friend).delete()
    return redirect('userprofile')
