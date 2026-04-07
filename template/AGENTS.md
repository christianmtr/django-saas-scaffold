# AGENTS.md — [[ project_name ]]

Guía para agentes de IA (OpenCode, Claude Code, Cursor, etc.).
**Leer completo antes de escribir cualquier línea de código.**

---

## Proyecto

| Campo | Valor |
|---|---|
| Nombre | [[ project_name ]] |
| Slug / schema raíz | [[ project_slug ]] |
| Dominio base | [[ base_domain ]] |
| Autor | [[ author_name ]] ([[ author_email ]]) |
| Versión | [[ version ]] |

**Stack**: Django 5 + DRF + django-tenants + drf-spectacular + django-auditlog[% if use_celery %] + Celery + Redis[% endif %]
**Testing**: pytest + pytest-django + Factory Boy
**Python**: [[ python_version ]] | **Package manager**: uv (backend), pnpm (frontend)

---

## Multi-tenancy — reglas no negociables

- Cada tenant = un schema PostgreSQL, accesible por `<tenant>.[[ base_domain ]]`
- El middleware de `django-tenants` setea el schema automáticamente. **Nunca manipules `search_path` a mano**
- Schema `public`: `Tenant`, `Domain`, planes, superadmins de plataforma → `SHARED_APPS`
- Schema de tenant: toda la lógica de negocio, usuarios del tenant → `TENANT_APPS`
- Migraciones: `migrate_schemas --shared` (public) o `migrate_schemas` (todos). **Nunca `migrate` a secas**
- Nunca hardcodear un nombre de schema

---

## Capas de código

```
Request → View → Service → Selector / Model → Response
```

### View (`views.py`) — solo HTTP
- Parsear request, llamar al service, devolver respuesta
- Sin SQL, sin lógica de negocio

### Service (`services.py`) — lógica de negocio
- Orquesta operaciones, puede llamar otros services
- Recibe datos ya validados (nunca un `request` object)
- Lanza excepciones de `apps/core/exceptions.py` o del dominio
- Nombrar con verbos: `create_reservation`, `cancel_booking`
[% if use_celery %]- Puede encolar tareas Celery para operaciones async (emails, notificaciones)
[% endif %]

### Selector (`selectors.py`) — solo lectura
- Queries que retornan QuerySets o valores. Nunca escribe
- Nombrar con `get_`: `get_available_slots`, `get_reservation_by_id`

### Serializer (`serializers.py`) — validación
- Separar entrada/salida: `ReservationCreateSerializer` / `ReservationSerializer`
- Validaciones de campo aquí; validaciones de negocio en el service
- Sin SQL ni lógica de negocio en `validate_*`, `create` o `update`

---

## Modelos

- Todo modelo de tenant hereda de `BaseModel` (`apps/core/models.py`)
- `BaseModel` provee: `id` (UUIDv4), `created_at`, `updated_at`
- Registrar modelos sensibles en auditlog:
  ```python
  from auditlog.registry import auditlog
  auditlog.register(MiModelo, exclude_fields=["updated_at"])
  ```
- Siempre definir `__str__` y `class Meta` con `verbose_name` / `verbose_name_plural`
- Nunca usar `id` auto-incremental en modelos de tenant

---

## Estructura de una app de dominio

```
apps/<dominio>/
├── models.py       ← Hereda de BaseModel
├── serializers.py  ← Separar Create/Update/Out
├── services.py     ← Lógica de negocio con verbos
├── selectors.py    ← Queries de solo lectura
├── views.py        ← Solo HTTP
├── urls.py
├── exceptions.py   ← Excepciones propias del dominio
├── constants.py    ← Constantes del dominio
├── admin.py
└── tests/
    ├── test_services.py
    ├── test_selectors.py
    └── test_views.py
```

Registrar la app en `TENANT_APPS` (settings) y sus URLs en `api/v1/router.py`.

---

## Testing

```python
# Test sin HTTP — usar tenant_context
def test_crear_reserva(tenant_context):
    reserva = crear_reserva(venue_id=..., fecha=...)
    assert reserva.estado == "pendiente"

# Test con HTTP — usar tenant_client
def test_endpoint_reservas(tenant_client):
    r = tenant_client.get("/api/v1/reservations/")
    assert r.status_code == 200
```

- Un test = un comportamiento. Nombre descriptivo: `test_cancel_reservation_notifies_guest`
- Tests independientes entre sí. Sin estado compartido
- Mockear externos con `pytest-mock`. Nunca llamadas reales en tests
- Factories en `tests/factories/<dominio>.py`, heredar de `DjangoModelFactory`
- Cobertura mínima: **80%** por app → `pytest --cov=apps -q`
[% if use_celery %]- Mockear tareas Celery en tests con `@pytest.mark.django_db` y `task.apply()` síncrono
[% endif %]

---

## API

- Prefijo: `/api/v1/`
- Siempre JSON. Paginación cursor-based con `next`, `previous`, `count`
- Documentar views no triviales con `@extend_schema` de drf-spectacular
- Errores: usar excepciones de `apps/core/exceptions.py`, DRF las serializa automáticamente

[% if use_celery %]
---

## Celery

- Tasks en `apps/<dominio>/tasks.py`
- Nombrar con verbos: `send_reservation_confirmation`, `cleanup_expired_slots`
- Tasks idempotentes siempre que sea posible
- No poner lógica de negocio en el task — llamar al service desde el task
- Usar `bind=True` y retry con backoff exponencial para tasks con I/O externo:
  ```python
  @shared_task(bind=True, max_retries=3)
  def send_email_task(self, reservation_id: str) -> None:
      try:
          send_reservation_confirmation(reservation_id)
      except Exception as exc:
          raise self.retry(exc=exc, countdown=2 ** self.request.retries)
  ```
[% endif %]

---

## Python

- `from __future__ import annotations` en todos los archivos
- Type hints en todas las funciones (parámetros + retorno)
- `ruff format` + `ruff check` deben pasar antes de todo commit
- Largo de línea: 88 | Imports: stdlib → third-party → local
- Secrets solo desde variables de entorno. Nunca hardcodeados

[% if use_frontend %]
---

## TypeScript / React

- TypeScript estricto (`"strict": true`). Sin `any`
- Solo componentes funcionales. Sin class components
- TanStack Query para estado del servidor, Zustand para UI global
- Llamadas API solo desde `src/api/` — nunca `fetch` directo en componentes
- Tailwind + shadcn/ui para estilos
- Nombres: `PascalCase` componentes, `camelCase` utils/hooks
[% endif %]

---

## Git

- Ramas desde `develop`: `feature/<slug>`, `fix/<slug>`, `chore/<slug>`
- Nunca commit directo a `main` o `develop`
- Conventional Commits: `feat(reservations): add cancel endpoint`
  - Tipos válidos: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`
- PRs pequeños y enfocados. Lint + tests verdes antes de merge

---

## Lo que los agentes NO deben hacer

- Lógica de negocio en views, serializers o modelos
- `migrate` sin `_schemas`
- Hardcodear schema names, tenant IDs o credenciales
- `id` auto-incremental en modelos de tenant
- Queries directas en views (sin pasar por selector o service)
- Instalar paquetes sin actualizar `pyproject.toml` o `package.json`
- Tests que dependan del orden de ejecución o compartan estado mutable
- `TODO` sin número de issue asociado
- Modificar migraciones existentes — siempre crear nuevas

---

## Glosario

| Término | Significado |
|---|---|
| **Tenant** | Cliente SaaS. Schema PostgreSQL propio, acceso por subdominio |
| **Platform user** | Superadmin cross-tenant. Vive en schema `public` |
| **Tenant user** | Usuario del negocio. Vive en el schema del tenant |
| **Selector** | Función de solo lectura que retorna datos de la BD |
| **Service** | Función que ejecuta lógica de negocio, puede escribir en BD |
[% if use_celery %]| **Task** | Tarea Celery async. Llama a un service, no contiene lógica propia |
[% endif %]
