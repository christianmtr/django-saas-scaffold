from __future__ import annotations

from django.db import models
from django_tenants.models import DomainMixin, TenantMixin


class Tenant(TenantMixin):
    """
    Cliente SaaS. Cada tenant tiene su propio schema PostgreSQL.
    Acceso por subdominio: <schema_name>.[[ base_domain ]]
    """

    name = models.CharField(max_length=100, verbose_name="nombre")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    auto_create_schema = True

    class Meta:
        verbose_name = "tenant"
        verbose_name_plural = "tenants"

    def __str__(self) -> str:
        return self.name


class Domain(DomainMixin):
    """Dominio o subdominio asociado a un tenant."""

    class Meta:
        verbose_name = "dominio"
        verbose_name_plural = "dominios"

    def __str__(self) -> str:
        return self.domain
