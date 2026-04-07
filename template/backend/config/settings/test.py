from __future__ import annotations

from .base import *  # noqa: F401, F403

DATABASES["default"]["NAME"] = env(  # noqa: F405, F821
    "DB_NAME_TEST", default="[[ project_slug ]]_test"
)

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
