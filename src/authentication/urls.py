from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.authlogin, name="login"),
    path("logout/", views.authlogout, name="logout"),
    path("registration/", views.authregistration, name="registration"),
    path("registration/verification/<name>/<token>/", views.authverification, name="verification"),
    path("reset_password/", views.reset_password, name="reset_password"),
    path(
        "reset_password/verification/<name>/<token>/",
        views.reset_pass_verification,
        name="reset_pass_verification",
    ),
    path("change_password/<name>/", views.change_password, name="change_password"),
]
