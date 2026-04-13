from __future__ import annotations

import factory
from factory.django import DjangoModelFactory

from apps.tenants.models import Domain, Tenant


class TenantFactory(DjangoModelFactory):
    schema_name = factory.Sequence(lambda n: f"tenant_{n}")
    name = factory.Sequence(lambda n: f"Tenant {n}")
    is_active = True

    class Meta:
        model = Tenant


class DomainFactory(DjangoModelFactory):
    tenant = factory.SubFactory(TenantFactory)
    domain = factory.LazyAttribute(
        lambda obj: f"{obj.tenant.schema_name}.[[ base_domain ]]"
    )
    is_primary = True

    class Meta:
        model = Domain
