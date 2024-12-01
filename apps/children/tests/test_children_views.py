import datetime

import pytest
from django.urls import reverse

from apps.children.factories import ChildrenFactory
from apps.children.models import Child

pytestmark = pytest.mark.django_db

CHILDREN_URL = reverse("apps.children:children-list")


@pytest.mark.parametrize(
    "client, expected_status_code",
    [
        ("unauthenticated_client", 401),
        ("authenticated_client", 200),
    ],
)
def test_children_get_view(user, client, expected_status_code, request):
    child = ChildrenFactory(created_by=user)
    client = request.getfixturevalue(client)
    response = client.get(CHILDREN_URL)

    assert response.status_code == expected_status_code

    if expected_status_code == 401:
        assert response.data["detail"] == "Authentication credentials were not provided."
    else:
        assert child.id == response.data["results"][0]["id"]


@pytest.mark.parametrize(
    "client, expected_status_code",
    [
        ("unauthenticated_client", 401),
        ("authenticated_client", 201),
    ],
)
def test_children_post_view(client, expected_status_code, request):
    data = {"family_name": "Test", "given_name": "User", "birth_date": "2024-01-01", "gender": "female"}
    client = request.getfixturevalue(client)
    response = client.post(CHILDREN_URL, data)

    assert response.status_code == expected_status_code

    if expected_status_code == 401:
        assert response.data["detail"] == "Authentication credentials were not provided."
    else:
        assert response.data["family_name"] == data["family_name"]
        assert response.data["given_name"] == data["given_name"]
        assert response.data["birth_date"] == data["birth_date"]
        assert response.data["gender"] == data["gender"]


@pytest.mark.parametrize(
    "client, expected_status_code",
    [
        ("unauthenticated_client", 401),
        ("authenticated_client", 200),
    ],
)
def test_children_patch_view(user, client, expected_status_code, request):
    child_by_user = ChildrenFactory(created_by=user)
    child_by_someone_else = ChildrenFactory()

    client = request.getfixturevalue(client)
    data = {
        "family_name": "Updated By",
        "given_name": "Test",
        "birth_date": datetime.date(2024, 12, 31),
        "gender": "male",
    }
    url = reverse("apps.children:children-detail", args=[child_by_user.id])

    response = client.patch(url, data)

    assert response.status_code == expected_status_code

    if expected_status_code == 401:
        assert response.data["detail"] == "Authentication credentials were not provided."
    else:
        updated_child = Child.objects.get(id=child_by_user.id)
        assert updated_child.family_name == data["family_name"]
        assert updated_child.given_name == data["given_name"]
        assert updated_child.birth_date == data["birth_date"]
        assert updated_child.gender == data["gender"]

        other_child = Child.objects.get(id=child_by_someone_else.id)
        assert other_child.family_name != data["family_name"]
        assert other_child.given_name != data["given_name"]
        assert other_child.birth_date != data["birth_date"]
        assert other_child.gender != data["gender"]


@pytest.mark.parametrize(
    "client, expected_status_code",
    [
        ("unauthenticated_client", 401),
        ("authenticated_client", 204),
    ],
)
def test_children_delete_view(user, client, expected_status_code, request):
    child_by_user = ChildrenFactory(created_by=user)
    child_by_someone_else = ChildrenFactory()

    client = request.getfixturevalue(client)
    url = reverse("apps.children:children-detail", args=[child_by_user.id])

    response = client.delete(url)

    assert response.status_code == expected_status_code

    if expected_status_code == 401:
        assert response.data["detail"] == "Authentication credentials were not provided."
    else:
        assert Child.objects.filter(id=child_by_someone_else.id).exists()
        assert not Child.objects.filter(id=child_by_user.id).exists()
