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
        "family_name": "Test",
        "given_name": "Kid",
        "birth_date": date(2011, 11, 11),
        "gender": "male",
        "created_by": user,
    }
    kid = Kid.objects.create(**kid_data)

    expected_kid = Kid.objects.get(id=kid.id)

    assert kid_data["family_name"] == expected_kid.family_name
    assert kid_data["given_name"] == expected_kid.given_name
    assert kid_data["birth_date"] == expected_kid.birth_date
    assert kid_data["gender"] in dict(Kid.GENDER_CHOICES)
    assert isinstance(kid_data["created_by"], User)
    assert Kid.objects.count() == 1


def test_create_kid_with_empty_created_by_field():
    kid = {
        "family_name": "Test",
        "given_name": "Kid2",
        "birth_date": "2012-11-11",
        "gender": "female",
    }

    with pytest.raises(IntegrityError):
        Kid.objects.create(**kid)
