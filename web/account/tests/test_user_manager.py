import dataclasses

import pytest
from django.test.client import Client

from account.models import User


@dataclasses.dataclass
class ExpectedCreateUser:
    email: str
    username: str = "Unknown"
    is_staff: bool = False
    is_superuser: bool = False


@pytest.mark.django_db
def test_create_user(client: Client) -> None:
    email = "test@example.com"
    password = "pass1234567890"

    result = User.objects.create_user(email, password)
    expected = ExpectedCreateUser(email=email)

    assert result.email == expected.email
    assert result.password is not None
    assert result.username == expected.username
    assert result.is_staff == expected.is_staff
    assert result.is_superuser == expected.is_superuser
