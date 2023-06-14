import pytest
from django.contrib import auth
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

"""
Tests for login
"""


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
    user = auth.get_user(client)
    assert user.is_anonymous is False


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


"""
Tests for logout
"""


@pytest.mark.django_db
def test_authlogout_get_request_from_authorized_user_successed(client, create_user, login_user):
    url = reverse("logout")
    response = client.get(url, follow=True)
    user = auth.get_user(client)
    assert response.status_code == 200
    assertTemplateUsed(response, "home.html")
    assert user.is_anonymous is True


@pytest.mark.django_db
def test_authlogout_get_request_from_unauthorized_user_redirect(client):
    url = reverse("logout")
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "login.html")
