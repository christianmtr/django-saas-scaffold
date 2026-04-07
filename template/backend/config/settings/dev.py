from __future__ import annotations

from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += ["django_extensions"]  # noqa: F405

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

INSTALLED_APPS += ["corsheaders"]  # noqa: F405
MIDDLEWARE.insert(2, "corsheaders.middleware.CorsMiddleware")  # noqa: F405
CORS_ALLOW_ALL_ORIGINS = True
