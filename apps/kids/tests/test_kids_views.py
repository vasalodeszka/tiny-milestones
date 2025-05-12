import datetime

import pytest
from django.urls import reverse

from apps.kids.factories import KidFactory
from apps.kids.models import Kid

pytestmark = pytest.mark.django_db

KIDS_URL = reverse("apps.kids:kids-list")


@pytest.mark.parametrize(
    "client, expected_status_code",
    [
        ("unauthenticated_client", 401),
        ("authenticated_client", 200),
    ],
)
def test_kids_get_view(user, client, expected_status_code, request):
    kid = KidFactory(created_by=user)
    client = request.getfixturevalue(client)
    response = client.get(KIDS_URL)

    assert response.status_code == expected_status_code

    if expected_status_code == 401:
        assert response.data["detail"] == "Authentication credentials were not provided."
    else:
        assert kid.id == response.data["results"][0]["id"]


@pytest.mark.parametrize(
    "client, expected_status_code",
    [
        ("unauthenticated_client", 401),
        ("authenticated_client", 201),
    ],
)
def test_kids_post_view(client, expected_status_code, request):
    data = {"full_name": "Test User", "date_of_birth": "2024-01-01", "gender": "female"}
    client = request.getfixturevalue(client)
    response = client.post(KIDS_URL, data)

    assert response.status_code == expected_status_code

    if expected_status_code == 401:
        assert response.data["detail"] == "Authentication credentials were not provided."
    else:
        assert response.data["full_name"] == data["full_name"]
        assert response.data["date_of_birth"] == data["date_of_birth"]
        assert response.data["gender"] == data["gender"]


@pytest.mark.parametrize(
    "client, expected_status_code",
    [
        ("unauthenticated_client", 401),
        ("authenticated_client", 200),
    ],
)
def test_kids_patch_view(user, client, expected_status_code, request):
    kid_by_user = KidFactory(created_by=user)
    kid_by_someone_else = KidFactory()

    client = request.getfixturevalue(client)
    data = {
        "full_name": "Updated By Test",
        "date_of_birth": datetime.date(2024, 12, 31),
        "gender": "male",
    }
    url = reverse("apps.kids:kids-detail", args=[kid_by_user.id])

    response = client.patch(url, data)

    assert response.status_code == expected_status_code

    if expected_status_code == 401:
        assert response.data["detail"] == "Authentication credentials were not provided."
    else:
        updated_kid = Kid.objects.get(id=kid_by_user.id)
        assert updated_kid.full_name == data["full_name"]
        assert updated_kid.date_of_birth == data["date_of_birth"]
        assert updated_kid.gender == data["gender"]

        other_kid = Kid.objects.get(id=kid_by_someone_else.id)
        assert other_kid.full_name != data["full_name"]
        assert other_kid.date_of_birth != data["date_of_birth"]
        assert other_kid.gender != data["gender"]


@pytest.mark.parametrize(
    "client, expected_status_code",
    [
        ("unauthenticated_client", 401),
        ("authenticated_client", 204),
    ],
)
def test_kids_delete_view(user, client, expected_status_code, request):
    kid_by_user = KidFactory(created_by=user)
    kid_by_someone_else = KidFactory()

    client = request.getfixturevalue(client)
    url = reverse("apps.kids:kids-detail", args=[kid_by_user.id])

    response = client.delete(url)

    assert response.status_code == expected_status_code

    if expected_status_code == 401:
        assert response.data["detail"] == "Authentication credentials were not provided."
    else:
        assert Kid.objects.filter(id=kid_by_someone_else.id).exists()
        assert not Kid.objects.filter(id=kid_by_user.id).exists()
