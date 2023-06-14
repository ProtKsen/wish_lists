import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


def test_authlogin_get_request_from_unauthorized_user_successed(client):
    url = reverse("login")
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "login.html")


@pytest.mark.django_db
def test_authlogin_get_request_from_authorized_user_redirect(client, create_user, login_user):
    url = reverse("login")
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "home.html")


@pytest.mark.django_db
def test_authlogin_post_request_valid_user_data_successed(client, create_user):
    url = reverse("login")
    form_data = {
        "username": "TestUser",
        "password": "TestPassword",
    }
    response = client.post(url, data=form_data, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "user_profile.html")


@pytest.mark.django_db
def test_authlogin_post_request_not_valid_username_show_error_message(client, create_user):
    url = reverse("login")
    form_data = {
        "username": "NotExistedUser",
        "password": "TestPassword",
    }
    response = client.post(url, data=form_data)
    assert response.status_code == 200
    assertTemplateUsed(response, "login.html")


@pytest.mark.django_db
def test_authlogin_post_request_not_valid_password_show_error_message(client, create_user):
    url = reverse("login")
    form_data = {
        "username": "TestUser",
        "password": "WrongPassword",
    }
    response = client.post(url, data=form_data)
    assert response.status_code == 200
    assertTemplateUsed(response, "login.html")
