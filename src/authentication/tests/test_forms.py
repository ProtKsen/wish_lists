import pytest
from django.contrib.auth.models import User

from authentication.forms import RegistrationForm


@pytest.mark.django_db
def test_registration_form_valid():
    form_data = {
        "username": "Test name",
        "email": "email@example.com",
        "password": "pass",
        "confirm_password": "pass",
    }
    form = RegistrationForm(data=form_data)
    assert form.is_valid() is True
