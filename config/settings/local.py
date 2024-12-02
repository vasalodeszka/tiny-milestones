# ruff: noqa: E501
from datetime import timedelta

from .base import *  # noqa: F403
from .base import env

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-wr-&wbqo@w6avw^6w_g)+c)w6*he^)ft090g20g0))d$_@_hph",
)

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", ".localhost", "0.0.0.0", "127.0.0.1"]  # noqa: S104

ADMIN_URL = "admin/"

SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(hours=24)  # noqa: F405
