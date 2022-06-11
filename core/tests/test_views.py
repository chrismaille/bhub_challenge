import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db(transaction=True)


def test_health_check_view(client):
    # Arrange

    # Act
    response = client.get(reverse("health_check"))

    # Assert
    assert response.status_code == 200


def test_health_check_readiness(client, admin_user):
    # Arrange

    # Act
    response = client.get(reverse("health_check_readiness"))

    # Assert
    assert response.status_code == 200
    assert response.json()["database"] == "OK (1)"
