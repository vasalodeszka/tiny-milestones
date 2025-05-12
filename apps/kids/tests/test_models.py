from datetime import date

import pytest
from django.db import IntegrityError

from apps.kids.models import Kid
from apps.users.factories import UserFactory
from apps.users.models import User

pytestmark = pytest.mark.django_db


def test_create_kid():
    user = UserFactory.create()
    kid_data = {
        "full_name": "Test Kid",
        "date_of_birth": date(2011, 11, 11),
        "gender": "male",
        "created_by": user,
    }
    kid = Kid.objects.create(**kid_data)

    expected_kid = Kid.objects.get(id=kid.id)

    assert kid_data["full_name"] == expected_kid.full_name
    assert kid_data["date_of_birth"] == expected_kid.date_of_birth
    assert kid_data["gender"] in dict(Kid.Gender.choices)
    assert isinstance(kid_data["created_by"], User)
    assert Kid.objects.count() == 1


def test_create_kid_with_empty_created_by_field():
    kid = {
        "full_name": "Test Kid2",
        "date_of_birth": "2012-11-11",
        "gender": "female",
    }

    with pytest.raises(IntegrityError):
        Kid.objects.create(**kid)
