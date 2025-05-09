# ruff: noqa: E501
from .base import *  # noqa: F403
from .base import env

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-wr-&wbqo@w6avw^6w_g)+c)w6*he^)ft090g20g0))d$_@_hph",
)

ADMIN_URL = "admin-prod/"

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = ["192.168.0.33", "localhost"]

# Gunicorn
WEB_CONCURRENCY = 4
