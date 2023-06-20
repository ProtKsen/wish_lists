import pytest
from django.contrib.auth.models import User

from authentication.models import HashSalt


@pytest.fixture
def create_user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user = User.objects.create_user(
            username="TestUser", email="test@test.com", password="TestPassword"
        )
        HashSalt.objects.create(user=user, salt="TestSalt")


@pytest.fixture
def login_user(django_db_setup, django_db_blocker, client, create_user):
    client.login(username="TestUser", password="TestPassword")
    return client


@pytest.fixture
def create_not_active_user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user = User.objects.create_user(
            username="NotActiveUser", email="test@test.com", password="TestPassword"
        )
        user.is_active = False
        user.save()
        HashSalt.objects.create(user=user, salt="TestSalt")
