from django.urls import path

from friends import views


urlpatterns = [
    path('', views.all_friends, name='all_friends'),
    path('<int:id>', views.friend_profile, name='friend_profile'),
    path('users', views.all_users, name='all_users'),
    path('send_request/<int:id>', views.send_request, name='send_request'),
    path('accept_request/<int:id>', views.accept_request, name='accept_request'),
    path('reject_request/<int:id>', views.reject_request, name='reject_request'),
    path('all_friend_requests', views.all_friend_requests, name='all_friend_requests'),
    path('delete_friend/<int:id>', views.delete_friend, name='delete_friend')
]
