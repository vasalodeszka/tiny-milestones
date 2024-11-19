import uuid

import pytest
from django.db import transaction

from apps.users.models import User

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "create_function,expected_staff,expected_superuser,expected_active",
    [(User.objects.create_user, False, False, True), (User.objects.create_superuser, True, True, True)],
)
@pytest.mark.parametrize("password", [("pass")])
def test_create_user(create_function, expected_staff, expected_superuser, expected_active, password):
    username = "user1"
    email = "user@example.com"
    first_name = "Jane"
    last_name = "Doe"

    with transaction.atomic():
        user = create_function(username, email=email, first_name=first_name, last_name=last_name, password=password)

    assert isinstance(user.uuid, uuid.UUID)
    assert user.uuid is not None
    assert user.username == username
    assert user.email == email
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.get_full_name() == f"{first_name} {last_name}"
    assert user.is_staff is expected_staff
    assert user.is_superuser is expected_superuser
    assert user.is_active is expected_active

    if password is not None:
        assert user.check_password(password)
