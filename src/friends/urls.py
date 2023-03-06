from django.urls import path

from friends import views


urlpatterns = [
    path('', views.all_friends, name='all_friends'),
    path('<int:id>', views.friend_profile, name='friend_profile')
]
