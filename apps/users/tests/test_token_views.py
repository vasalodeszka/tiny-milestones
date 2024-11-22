import pytest
from django.urls import reverse
from rest_framework import status

from apps.users.factories import UserFactory

TOKEN_OBTAIN_URL = reverse("apps.users:token_obtain_pair")
TOKEN_REFRESH_URL = reverse("apps.users:token_refresh")
TOKEN_VERIFY_URL = reverse("apps.users:token_verify")
TOKEN_BLACKLIST_URL = reverse("apps.users:token_blacklist")


pytestmark = pytest.mark.django_db


def attempt_login(url, user, unauthenticated_client, invalid=False):
    new_user = UserFactory.create(password=user.password)

    if invalid:
        data = {"username": "invalid", "password": "invalid"}
    else:
        data = {"username": new_user.username, "password": user.password}

    response = unauthenticated_client.post(url, data, format="json")

    return response


def test_custom_token_obtain_pair_view(user, unauthenticated_client):
    response = attempt_login(TOKEN_OBTAIN_URL, user, unauthenticated_client)

    assert response.status_code == status.HTTP_200_OK
    assert "refresh" not in response.data
    assert "refresh_token" in response.cookies
    assert "access" in response.data


def test_custom_token_obtain_pair_view_invalid_credentials(user, unauthenticated_client):
    response = attempt_login(TOKEN_OBTAIN_URL, user, unauthenticated_client, invalid=True)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "refresh" not in response.data
    assert "refresh_token" not in response.cookies
    assert "access" not in response.data
    assert response.data["detail"] == "No active account found with the given credentials"


def test_custom_token_refresh_view(user, unauthenticated_client):
    response = attempt_login(TOKEN_OBTAIN_URL, user, unauthenticated_client)

    refresh_token = response.cookies.get("refresh_token")
    assert refresh_token is not None

    url = TOKEN_REFRESH_URL
    refresh_cookie_header = f"refresh_token={refresh_token}"
    response = unauthenticated_client.post(url, HTTP_Cookie=refresh_cookie_header, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


def test_custom_token_refresh_view_without_token(unauthenticated_client):
    url = TOKEN_REFRESH_URL
    response = unauthenticated_client.post(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["refresh"][0] == "This field may not be null."
    assert "access" not in response.data


def test_token_verify_view(user, unauthenticated_client):
    response = attempt_login(TOKEN_OBTAIN_URL, user, unauthenticated_client)

    access_token = response.data.get("access")
    assert access_token is not None

    url = TOKEN_VERIFY_URL
    data = {"token": access_token}
    response = unauthenticated_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {}


def test_token_verify_view_without_token(unauthenticated_client):
    url = TOKEN_VERIFY_URL
    response = unauthenticated_client.post(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["token"][0] == "This field is required."
    assert "access" not in response.data


def test_token_blacklist_view(user, unauthenticated_client):
    response = attempt_login(TOKEN_OBTAIN_URL, user, unauthenticated_client)
    assert response.status_code == 200

    refresh_token = response.cookies.get("refresh_token")
    assert refresh_token is not None

    unauthenticated_client.cookies["refresh_token"] = refresh_token

    response = unauthenticated_client.post(TOKEN_BLACKLIST_URL, format="json")
    assert response.status_code == 200

    # Check if cookie is deleted in response
    response = unauthenticated_client.post(TOKEN_REFRESH_URL)
    assert response.status_code == 400
    assert response.data["refresh"][0] == "This field may not be blank."

    # Check if re-using the same refresh token is not possible
    unauthenticated_client.cookies["refresh_token"] = refresh_token
    response = unauthenticated_client.post(TOKEN_REFRESH_URL)
    assert response.status_code == 401
    assert response.data["detail"] == "Token is blacklisted"


def test_token_blacklist_view_with_invalid_token(unauthenticated_client):
    unauthenticated_client.cookies["refresh_token"] = "invalid_token"
    response = unauthenticated_client.post(TOKEN_BLACKLIST_URL, format="json")

    assert response.status_code == 401
    assert response.data["detail"] == "Token is invalid or expired"
