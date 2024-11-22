import pytest
from django.urls import reverse

from apps.users.factories import UserFactory
from apps.users.models import User

pytestmark = pytest.mark.django_db

USERS_URL = reverse("apps.users:users-list")


@pytest.mark.parametrize(
    "client, expected_status_code",
    [
        ("unauthenticated_client", 401),
        ("authenticated_client", 200),
    ],
)
def test_user_get_view(client, expected_status_code, request):
    UserFactory.create()
    UserFactory.create()

    client = request.getfixturevalue(client)
    response = client.get(USERS_URL)

    assert response.status_code == expected_status_code
    if expected_status_code == 401:
        assert response.data["detail"] == "Authentication credentials were not provided."
    else:
        assert "password" not in response.data["results"][0]
        assert len(response.data["results"]) == 3


@pytest.mark.parametrize(
    "client, expected_status_code, data",
    [
        ("unauthenticated_client", 401, {"username": "test", "password": "test"}),
        ("unauthenticated_client", 401, {}),
        ("authenticated_client", 201, {"username": "test", "password": "test"}),
        ("authenticated_client", 400, {}),
    ],
)
def test_user_post_view(client, expected_status_code, data, request):
    client = request.getfixturevalue(client)
    response = client.post(USERS_URL, data)

    assert response.status_code == expected_status_code
    match response.status_code:
        case 201:
            assert response.data["username"] == data["username"]
            assert "password" not in response.data
            assert User.objects.filter(username=data["username"]).exists()
        case 400:
            assert response.data["username"][0] == "This field is required."
        case 401:
            assert response.data["detail"] == "Authentication credentials were not provided."


@pytest.mark.parametrize(
    "client, expected_status_code",
    [
        ("unauthenticated_client", 401),
        ("authenticated_client", 204),
    ],
)
def test_user_delete_view(client, expected_status_code, request):
    user = UserFactory.create()

    client = request.getfixturevalue(client)
    url = reverse("apps.users:users-detail", args=[user.uuid])
    response = client.delete(url)

    assert response.status_code == expected_status_code
    match response.status_code:
        case 204:
            assert not User.objects.filter(uuid=user.uuid).exists()
        case 401:
            assert response.data["detail"] == "Authentication credentials were not provided."


@pytest.mark.parametrize(
    "client, expected_status_code, data",
    [
        (
            "unauthenticated_client",
            401,
            {"username": "changed_username", "first_name": "changed_first_name", "last_name": "changed_last_name"},
        ),
        (
            "authenticated_client",
            200,
            {"username": "changed_username", "first_name": "changed_first_name", "last_name": "changed_last_name"},
        ),
    ],
)
def test_user_patch_view(client, expected_status_code, data, request):
    user = UserFactory.create(username="test_user", first_name="test", last_name="name")

    client = request.getfixturevalue(client)
    url = reverse("apps.users:users-detail", args=[user.uuid])
    response = client.patch(url, data)

    assert response.status_code == expected_status_code
    match response.status_code:
        case 200:
            assert response.data["username"] == data["username"]
            assert response.data["first_name"] == data["first_name"]
            assert response.data["last_name"] == data["last_name"]
            assert User.objects.get(uuid=user.uuid).username == data["username"]
        case 401:
            assert response.data["detail"] == "Authentication credentials were not provided."
