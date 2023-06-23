from io import BytesIO

import pytest
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.urls import reverse
from PIL import Image
from pytest_django.asserts import assertTemplateUsed

from userprofile.models import Wish
from userprofile.tests.factories import WishFactory

"""
Tests for userprofile
"""


@pytest.mark.django_db
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
    user.save()
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


@pytest.mark.django_db
@pytest.mark.parametrize("n", [0, 5])
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


"""
Tests for addwish
"""


@pytest.mark.django_db
def test_addwish_get_request_from_unauthorized_user_redirect(client):
    url = reverse("addwish")
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "login.html")


@pytest.mark.django_db
def test_addwish_get_request_from_authorized_not_active_user_redirect(
    client, create_user, login_user
):
    user = User.objects.get(username="TestUser")
    user.is_active = False
    user.save()
    url = reverse("addwish")
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assertTemplateUsed(response, "login.html")


@pytest.mark.django_db
def test_addwish_get_request_from_authorized_active_user_successed(
    client, create_user, login_user
):
    url = reverse("addwish")
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "add_wish.html")


@pytest.mark.django_db
def test_addwish_post_request_valid_form_without_image_successed(client, create_user, login_user):
    url = reverse("addwish")
    form_data = {
        "title": "New wish",
        "link": "link",
        "description": "Test description",
        "type": "General",
    }
    response = client.post(url, data=form_data, follow=True)
    wish = Wish.objects.get(title="New wish")

    assert response.status_code == 200
    assertTemplateUsed(response, "user_profile.html")
    assert wish.title == "New wish"
    assert wish.link == "link"
    assert wish.description == "Test description"
    assert wish.type == "General"
    assert wish.image == "img/wish_default.jpg"


""" do later
@pytest.mark.django_db
def test_addwish_post_request_with_image_successed(client, create_user, login_user):
    url = reverse("addwish")
    image_data = BytesIO()
    image = Image.new('RGB', (100, 100), 'white')
    image.save(image_data, format='png')
    image_data.seek(0)
    form_data = {
        "title": "New wish",
        "link": "link",
        "description": "Test description",
        "type": "General",
        "file": TemporaryUploadedFile("example.png", image_data.read(), size=10, charset="utf8"),
    }
    response = client.post(url, data=form_data, format='multipart', follow=True)
    wish = Wish.objects.get(title="New wish")

    assert response.status_code == 200
    assertTemplateUsed(response, "user_profile.html")
    assert wish.image == "img/example.png"
"""


@pytest.mark.django_db
def test_addwish_post_request_not_valid_form_show_error_message(client, create_user, login_user):
    url = reverse("addwish")
    form_data = {"not_valid": "not_valid"}
    response = client.post(url, data=form_data, follow=True)
    messages = list(response.context["messages"])

    assert response.status_code == 200
    assertTemplateUsed(response, "add_wish.html")
    assert len(messages) == 1
    assert str(messages[0]) == "Данные указаны неверно"


"""
Tests for delete_wish
"""


@pytest.mark.django_db
def test_delete_wish_get_request_from_unauthorized_user_redirect(client, create_user):
    user = User.objects.get(username="TestUser")
    wish = Wish.objects.create(
        user=user, title="New wish", link="link", description="Test description", type="General"
    )
    url = reverse("deletewish", kwargs={"id": wish.id})
    response = client.get(url, follow=True)

    assert response.status_code == 200
    assertTemplateUsed(response, "login.html")


@pytest.mark.django_db
def test_delete_wish_get_request_from_authorized_user_not_existed_wish_failed(
    client, create_user, login_user
):
    url = reverse("deletewish", kwargs={"id": 123})
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_wish_get_request_from_authorized_user_permission_denied_failed(
    client, create_user, login_user
):
    user = User.objects.create_user(
        username="NewUser", email="test@test.com", password="TestPassword"
    )
    wish = Wish.objects.create(
        user=user, title="New wish", link="link", description="Test description", type="General"
    )
    url = reverse("deletewish", kwargs={"id": wish.id})
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_wish_get_request_successed(client, create_user, login_user):
    user = User.objects.get(username="TestUser")
    wish = Wish.objects.create(
        user=user, title="New wish", link="link", description="Test description", type="General"
    )
    url = reverse("deletewish", kwargs={"id": wish.id})
    response = client.get(url, follow=True)

    assert response.status_code == 200
    assertTemplateUsed(response, "user_profile.html")
