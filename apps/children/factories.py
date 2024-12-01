from datetime import date

from factory import Faker, Iterator, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDate, FuzzyText

from apps.children.models import Child
from apps.users.factories import UserFactory


class ChildrenFactory(DjangoModelFactory):
    family_name = Faker("last_name")
    given_name = Faker("first_name")
    birth_date = FuzzyDate(start_date=date(2020, 1, 1), end_date=date(2025, 1, 1))
    gender = Iterator([choice[0] for choice in getattr(Child, "GENDER_CHOICES", [])])
    bio = FuzzyText(prefix="bio_")
    created_by = SubFactory(UserFactory)

    class Meta:
        model = Child
