from django.test.client import Client
from django.urls import reverse


def test_status_200(client: Client) -> None:
    response = client.get(reverse("config:index"))
    assert response.status_code == 200
