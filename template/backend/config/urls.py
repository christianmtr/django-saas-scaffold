from __future__ import annotations

from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# ---------------------------------------------------------------------------
# URLs para schemas de tenant.
# Registrar las URLs de cada app de dominio aquí:
#
#   from apps.tenant.reservations.urls import urlpatterns as reservations_urls
#   urlpatterns += reservations_urls
#
# Prefijo sugerido por app: path("api/v1/reservations/", include(...))
# ---------------------------------------------------------------------------

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # Apps de tenant — agregar aquí
]
