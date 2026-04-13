# [[ project_name ]]

[[ project_description ]]

**Autor**: [[ author_name ]] — [[ author_email ]]
**Versión**: [[ version ]] | **Dominio base**: [[ base_domain ]]

## Stack

- **Backend**: Django 5 + Django REST Framework + django-tenants
- **API Docs**: drf-spectacular (OpenAPI 3 / Swagger)
- **Auditoría**: django-auditlog
- **Testing**: pytest + Factory Boy
[% if use_celery %]- **Tareas async**: Celery + Redis
[% endif %][% if use_frontend %]- **Frontend**: React 19 + Vite + TypeScript
[% endif %]- **Infra**: Docker + docker-compose + GitHub Actions

## Inicio rápido

```bash
# 1. Variables de entorno
cp backend/.env.example backend/.env
# Editar .env con las credenciales reales

# 2. Levantar servicios
docker compose -f compose.dev.yml up --build

# 3. Migraciones (schema público)
docker compose -f compose.dev.yml exec backend \
  python manage.py migrate_schemas --shared

# 4. Superusuario de plataforma
docker compose -f compose.dev.yml exec backend \
  python manage.py createsuperuser
```

[% if use_frontend %]
## Frontend

```bash
cd frontend
pnpm install
pnpm dev   # http://localhost:5173
```

El cliente TypeScript se genera automáticamente desde el schema OpenAPI:

```bash
pnpm run generate-client
```
[% endif %]

## Comandos frecuentes

```bash
# Migraciones para todos los tenants
docker compose -f compose.dev.yml exec backend \
  python manage.py migrate_schemas

# Tests
docker compose -f compose.dev.yml exec backend \
  pytest --cov=apps -q

# Lint
docker compose -f compose.dev.yml exec backend \
  ruff check . && ruff format --check .
```

## Multi-tenancy

- Cada tenant = un schema PostgreSQL
- Acceso por subdominio: `<tenant>.[[ base_domain ]]`
- Schema `public`: tenants, dominios, planes, superadmins
- Schema de tenant: toda la lógica de negocio

## Estructura

```
.
├── backend/
│   ├── apps/
│   │   ├── shared/         ← SHARED_APPS (schema public)
│   │   │   ├── core/       ← BaseModel, excepciones base
│   │   │   └── tenants/    ← Tenant + Domain
│   │   └── tenant/         ← TENANT_APPS (schema por cliente)
│   │       └── <dominio>/  ← Apps de negocio (agregar aquí)
│   ├── config/
│   │   ├── settings/       ← base / dev / prod / test
│   │   ├── urls.py         ← Registrar URLs de cada app aquí
│   │   └── urls_public.py
│   └── tests/
[% if use_frontend %]├── frontend/src/
│   ├── api/                ← Cliente tipado (auto-generado)
│   ├── components/
│   ├── hooks/
│   └── stores/
[% endif %]├── compose.dev.yml
├── compose.prod.yml
└── AGENTS.md
```

## Actualizar desde el scaffold base

```bash
copier update
```

## Convenciones

Ver `AGENTS.md` para las convenciones completas de código, capas y testing.
