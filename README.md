# django-saas-scaffold

Template [Copier](https://copier.readthedocs.io) para proyectos SaaS multi-tenant con Django.

## Crear un proyecto nuevo

```bash
# Requiere copier instalado: pip install copier
copier copy gh:christianmtr/django-saas-scaffold mi-proyecto

# Sin instalarlo (con pipx):
pipx run copier copy gh:christianmtr/django-saas-scaffold mi-proyecto
```

## Preguntas que hace Copier

| Variable | Descripción | Ejemplo |
|---|---|---|
| `project_name` | Nombre del proyecto | `RestaurantHub` |
| `project_slug` | Slug para schema y módulos | `restauranthub` |
| `project_description` | Descripción corta | `SaaS de reservas` |
| `author_name` | Nombre o empresa | `Christian` |
| `author_email` | Email de contacto | `hi@ejemplo.pe` |
| `github_username` | Usuario GitHub para URLs | `cperez` |
| `timezone` | Timezone del servidor | `America/Lima` |
| `base_domain` | Dominio base (tenants = subdominio.base_domain) | `miapp.pe` |
| `version` | Versión inicial | `0.1.0` |
| `python_version` | Versión de Python | `3.12` |

## Componentes opcionales

| Componente | Variable | Default |
|---|---|---|
| Celery + Redis | `use_celery` | `false` |
| Frontend React + Vite + TS | `use_frontend` | `true` |

## Siempre incluidos (no son opcionales)

- Docker + docker-compose (dev y prod)
- GitHub Actions CI/CD
- django-auditlog
- drf-spectacular (OpenAPI)
- pytest + Factory Boy

## Actualizar proyectos existentes

Esta es la killer feature de Copier sobre Cookiecutter.
Cuando mejoras el scaffold y quieres propagar los cambios:

```bash
# Desde la raíz del proyecto generado
copier update

# Copier hace diff entre la versión que se usó y la actual,
# aplica los cambios y pide resolver conflictos si los hay.
```

## Sintaxis Jinja2 del template

Delimitadores personalizados para no conflictuar con Django templates:

| Propósito | Sintaxis |
|---|---|
| Variable | `[[ variable ]]` |
| Bloque condicional | `[% if condicion %]...[% endif %]` |
| Comentario | `[# esto no se renderiza #]` |

## Estructura del repo

```
django-saas-scaffold/
├── copier.yml              ← Preguntas y configuración
├── README_SCAFFOLD.md      ← Este archivo (no se copia al proyecto)
└── template/               ← Archivos que se copian y renderizan
    ├── README.md
    ├── AGENTS.md
    ├── compose.dev.yml
    ├── compose.prod.yml
    ├── .github/workflows/ci.yml
    ├── backend/
    │   ├── Dockerfile
    │   ├── Dockerfile.dev
    │   ├── pyproject.toml
    │   ├── manage.py
    │   ├── .env.example
    │   ├── config/
    │   │   ├── settings/{base,dev,prod,test}.py
    │   │   ├── urls.py
    │   │   ├── urls_public.py
    │   │   └── wsgi.py
    │   ├── apps/
    │   │   ├── core/       ← BaseModel, excepciones
    │   │   └── tenants/    ← Tenant, Domain
    │   ├── api/v1/router.py
    │   └── tests/
    │       ├── conftest.py
    │       └── factories/
    └── frontend/           ← Solo si use_frontend=true
        ├── package.json
        ├── vite.config.ts
        ├── tsconfig.json
        └── src/
```

## Versionado del scaffold

Cada mejora significativa → nuevo tag:

```bash
git tag v1.1.0
git push --tags
```

Los proyectos generados pueden hacer `copier update --vcs-ref v1.1.0`
para actualizarse a una versión específica.
