import pytest
from django.contrib import auth
from django.contrib.auth.models import User
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


"""
Tests for authregistration
"""


def test_authregistration_get_request_from_unauthorized_user_successed(client):
    url = reverse("registration")
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "registration.html")


@pytest.mark.django_db
def test_authregistration_get_request_from_authorized_user_redirect(
    client, create_user, login_user
):
    url = reverse("registration")
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "home.html")


@pytest.mark.django_db
def test_authregistration_post_request_valid_new_user_redirect(client):
    url = reverse("registration")
    form_data = {
        "username": "NewUser",
        "email": "new@example.com",
        "password": "NewPassword",
        "confirm_password": "NewPassword",
    }
    response = client.post(url, data=form_data, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "verification.html")

    user = User.objects.get(username="NewUser")
    assert user.is_active is False


@pytest.mark.django_db
def test_authregistration_post_request_not_valid_username_show_error_massage(client, create_user):
    url = reverse("registration")
    form_data = {
        "username": "TestUser",
        "email": "new@example.com",
        "password": "NewPassword",
        "confirm_password": "NewPassword",
    }
    response = client.post(url, data=form_data, follow=True)
    messages = list(response.context["messages"])

    assert response.status_code == 200
    assertTemplateUsed(response, "registration.html")
    assert len(messages) == 1
    assert str(messages[0]) == "Пользователь с таким именем уже существует"


@pytest.mark.django_db
def test_authregistration_post_request_not_valid_email_show_error_massage(client, create_user):
    url = reverse("registration")
    form_data = {
        "username": "NewUser",
        "email": "test@test.com",
        "password": "NewPassword",
        "confirm_password": "NewPassword",
    }
    response = client.post(url, data=form_data, follow=True)
    messages = list(response.context["messages"])

    assert response.status_code == 200
    assertTemplateUsed(response, "registration.html")
    assert len(messages) == 1
    assert str(messages[0]) == "Пользователь с таким email уже существует"


"""
Tests for authverification
"""


def test_authverification_get_request_successed(client):
    url = reverse("verification", kwargs={"name": "name", "token": "token"})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_authverification_post_request_not_existed_user_redirect(client, create_user):
    url = reverse("verification", kwargs={"name": "NewUser", "token": "token"})
    form_data = {"verification_code": 1234}
    response = client.post(url, data=form_data, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "home.html")


@pytest.mark.django_db
def test_authverification_post_request_not_valid_type_of_code_show_error_message(
    client, create_user
):
    url = reverse("verification", kwargs={"name": "TestUser", "token": "token"})
    form_data = {"verification_code": "not_valid_code"}
    response = client.post(url, data=form_data, follow=True)
    messages = list(response.context["messages"])
    assert response.status_code == 200
    assertTemplateUsed(response, "verification.html")
    assert len(messages) == 1
    assert str(messages[0]) == "Код должен содержать 4 цифры."


@pytest.mark.django_db
def test_authverification_post_request_not_valid_code_show_error_message(client, create_user):
    url = reverse("verification", kwargs={"name": "TestUser", "token": "token"})
    form_data = {"verification_code": 1234}
    response = client.post(url, data=form_data, follow=True)
    messages = list(response.context["messages"])
    assert response.status_code == 200
    assertTemplateUsed(response, "verification.html")
    assert len(messages) == 1
    assert str(messages[0]) == "Введен неверный код."


"""
Tests for reset_password
"""


def test_reset_password_get_request_successed(client):
    url = reverse("reset_password")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_reset_password_post_request_valid_email_redirect(client, create_user):
    url = reverse("reset_password")
    form_data = {"email": "test@test.com"}
    response = client.post(url, data=form_data, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "reset_pass_verification.html")


@pytest.mark.django_db
def test_reset_password_post_request_not_existed_email_redirect(client, create_user):
    url = reverse("reset_password")
    form_data = {"email": "not_existed@test.com"}
    response = client.post(url, data=form_data, follow=True)
    messages = list(response.context["messages"])
    assert response.status_code == 200
    assertTemplateUsed(response, "reset_password.html")
    assert len(messages) == 1
    assert str(messages[0]) == "Пользователя с таким email не существует"
