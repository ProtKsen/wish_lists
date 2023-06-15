import pytest
from django.contrib.auth.models import User


@pytest.fixture
def create_user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return User.objects.create_user(
            username="TestUser", email="test@test.com", password="TestPassword"
        )


@pytest.fixture
def login_user(django_db_setup, django_db_blocker, client, create_user):
    client.login(username="TestUser", password="TestPassword")
    return client
