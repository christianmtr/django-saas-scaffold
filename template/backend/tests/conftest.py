from __future__ import annotations

import pytest
from django_tenants.test.client import TenantClient
from django_tenants.utils import schema_context

from apps.tenants.models import Domain, Tenant


@pytest.fixture(scope="function")
def tenant(db):
    """
    Crea un schema de tenant aislado para el test.
    Se destruye automáticamente al finalizar.
    """
    t = Tenant(schema_name="test_[[ project_slug ]]", name="Test Tenant")
    t.save(verbosity=0)
    Domain.objects.create(
        domain="test.[[ base_domain ]]",
        tenant=t,
        is_primary=True,
    )
    yield t
    t.delete(force_drop=True)


@pytest.fixture
def tenant_client(tenant):
    """
    Cliente HTTP con el tenant activado.
    Reemplaza al `client` estándar de pytest-django en este proyecto.
    """
    return TenantClient(tenant)


@pytest.fixture
def tenant_context(tenant):
    """
    Activa el schema del tenant para tests sin HTTP.

    Uso:
        def test_crear_algo(tenant_context):
            MiModelo.objects.create(...)
    """
    with schema_context(tenant.schema_name):
        yield tenant
