from datetime import date

import pytest
from django.db import IntegrityError

from apps.children.models import Child
from apps.users.factories import UserFactory
from apps.users.models import User

pytestmark = pytest.mark.django_db


def test_create_child():
    user = UserFactory.create()
    child_data = {
        "family_name": "Test",
        "given_name": "Child",
        "birth_date": date(2011, 11, 11),
        "gender": "male",
        "created_by": user,
    }
    child = Child.objects.create(**child_data)

    expected_child = Child.objects.get(id=child.id)

    assert child_data["family_name"] == expected_child.family_name
    assert child_data["given_name"] == expected_child.given_name
    assert child_data["birth_date"] == expected_child.birth_date
    assert child_data["gender"] in dict(Child.GENDER_CHOICES)
    assert isinstance(child_data["created_by"], User)
    assert Child.objects.count() == 1


def test_create_child_with_empty_created_by_field():
    child = {
        "family_name": "Test",
        "given_name": "Child2",
        "birth_date": "2012-11-11",
        "gender": "female",
    }

    with pytest.raises(IntegrityError):
        Child.objects.create(**child)
