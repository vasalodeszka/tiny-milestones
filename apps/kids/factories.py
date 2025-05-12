from datetime import date

from factory import Faker, Iterator, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDate, FuzzyText

from apps.kids.models import Kid
from apps.users.factories import UserFactory


class KidFactory(DjangoModelFactory):
    full_name = Faker("name")
    date_of_birth = FuzzyDate(start_date=date(2020, 1, 1), end_date=date(2025, 1, 1))
    gender = Iterator([choice[0] for choice in Kid.Gender.choices])
    bio = FuzzyText(prefix="bio_")
    created_by = SubFactory(UserFactory)

    class Meta:
        model = Kid
