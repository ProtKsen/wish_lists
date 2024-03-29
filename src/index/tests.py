import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_home_get_request_successed(client):
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "home.html")
