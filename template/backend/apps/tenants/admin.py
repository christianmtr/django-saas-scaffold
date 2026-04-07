from __future__ import annotations

from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from .models import Domain, Tenant


class DomainInline(admin.TabularInline):
    model = Domain
    extra = 1


@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ["name", "schema_name", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["name", "schema_name"]
    inlines = [DomainInline]
