import pytest
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from userprofile.tests.factories import WishFactory

"""
Tests for userprofile
"""


def test_userprofile_get_request_from_unauthorized_user_redirect(client):
    url = reverse("userprofile")
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "login.html")


@pytest.mark.django_db
def test_userprofile_get_request_from_authorized_not_active_user_redirect(
    client, create_user, login_user
):
    user = User.objects.get(username="TestUser")
    user.is_active = False
    url = reverse("userprofile")
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "login.html")


@pytest.mark.django_db
def test_userprofile_get_request_from_authorized_active_user_successed(
    client, create_user, login_user
):
    url = reverse("userprofile")
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "user_profile.html")


@pytest.mark.parametrize("n", [0, 5])
@pytest.mark.django_db
def test_userprofile_show_all_wishes_for_exact_user(client, create_user, login_user, n):
    test_user = User.objects.get(username="TestUser")
    for _ in range(n):
        wish = WishFactory(user=test_user)
        wish.save()

    new_user = User.objects.create(username="New_User", password="pass")
    for _ in range(n):
        wish = WishFactory(user=new_user)
        wish.save()

    url = reverse("userprofile")
    response = client.get(url)
    assert response.status_code == 200
    assert len(list(response.context["wishes"])) == n
