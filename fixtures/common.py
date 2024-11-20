import pytest
from rest_framework.test import APIClient

from apps.users.factories import UserFactory


@pytest.fixture
def user(db):  # noqa: ARG001
    """Creates a user"""
    return UserFactory.create()


@pytest.fixture
def unauthenticated_client(user):
    """DRF API test client that is not authenticated with a user"""
    return APIClient()


@pytest.fixture
def authenticated_client(user):
    """DRF API test client that is authenticated with the user"""
    client = APIClient()
    client.force_authenticate(user=user)
    return client
