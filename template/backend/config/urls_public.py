from __future__ import annotations

from django.contrib import admin
from django.urls import path

# URLs exclusivas del schema public (landing, registro de tenants, etc.)
urlpatterns = [
    path("admin/", admin.site.urls),
]
