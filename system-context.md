# System Context — Float Plan API

## Purpose

REST API backend for the [float_plan](https://github.com/lackmannicholas/float_plan) frontend application. Allows boaters to create and manage float plans — safety documents filed before heading out on the water.

## Tech Stack

| Layer | Technology | Version Constraint |
|---|---|---|
| Language | Python 3.12+ | Uses `X \| None` union syntax |
| Framework | FastAPI | >= 0.115.0 |
| Server | Uvicorn | >= 0.30.0 |
| ORM | SQLAlchemy 2.x (Mapped column style) | >= 2.0.0 |
| Validation | Pydantic v2 | >= 2.0.0 |
| Database | SQLite (file-based, `float_plans.db`) | — |
| HTTP Client | httpx | >= 0.27.0 |
| Testing | pytest + FastAPI `TestClient` | pytest >= 8.0.0 |

## Project Structure

```
float_plan_api/
├── app/
│   ├── main.py            # FastAPI app, middleware, health check
│   ├── database.py        # SQLAlchemy engine, session factory, get_db dependency
│   ├── models.py          # ORM models (FloatPlan, Passenger, EmergencyContact)
│   ├── schemas.py         # Pydantic request/response schemas
│   ├── crud.py            # Database CRUD operations
│   └── routers/
│       └── float_plans.py # /float_plans endpoint routes
├── tests/
│   └── test_float_plans.py
├── requirements.txt
└── system-context.md      # (this file)
```

## Coding Conventions

- **ORM models** use SQLAlchemy 2.x `Mapped[]` / `mapped_column()` declarative style.
- **Pydantic schemas** follow the Base → Create / Update / Read pattern (e.g., `FloatPlanBase`, `FloatPlanCreate`, `FloatPlanRead`).
- **Routers** live under `app/routers/` and are registered in `app/main.py` via `app.include_router()`.
- **CRUD functions** live in `app/crud.py` and accept a SQLAlchemy `Session` as the first argument.
- **Database sessions** are injected through FastAPI's `Depends(get_db)` pattern.
- **Type hints** are required on all function signatures. Use Python 3.12+ union syntax (`X | None`) instead of `Optional[X]`.
- **Imports** use the `from app import ...` absolute package style.

## Database

- Default: SQLite at `./float_plans.db` (created automatically via `Base.metadata.create_all`).
- Connection string is defined in `app/database.py` (`SQLALCHEMY_DATABASE_URL`).
- No migration tool is currently configured — schema changes are applied via `create_all` on startup.

### Current Models

| Model | Table | Key Relationships |
|---|---|---|
| `FloatPlan` | `float_plans` | has many `Passenger`, has many `EmergencyContact` (cascade delete-orphan) |
| `Passenger` | `passengers` | belongs to `FloatPlan` |
| `EmergencyContact` | `emergency_contacts` | belongs to `FloatPlan` |

## API Endpoints

All routes are registered under the `/float_plans` prefix.

| Method | Path | Status | Description |
|---|---|---|---|
| `GET` | `/` | 200 | Health check |
| `GET` | `/float_plans/` | 200 | List float plans (summary view, paginated) |
| `POST` | `/float_plans/` | 201 | Create a new float plan |
| `GET` | `/float_plans/{id}` | 200 | Get a single float plan with passengers & contacts |
| `PUT` | `/float_plans/{id}` | 200 | Update a float plan (partial fields accepted) |
| `DELETE` | `/float_plans/{id}` | 204 | Delete a float plan |

Standard error responses: `404` for not found, `422` for validation errors.

## Testing

- **Framework:** pytest
- **HTTP client:** `fastapi.testclient.TestClient`
- **Test database:** In-memory or file-based SQLite (`test_float_plans.db`), fully recreated per test via `autouse` fixtures.
- **DB override:** Tests override the `get_db` dependency to use an isolated session.
- **Test organization:** Tests are grouped into classes by feature area (e.g., `TestCreateFloatPlan`, `TestUpdateFloatPlan`).
- **Run tests:**
  ```bash
  pytest
  ```
- **All new endpoints, functions, or components must have corresponding unit and integration tests.**

## Configuration

| Environment Variable | Default | Description |
|---|---|---|
| `CORS_ALLOWED_ORIGINS` | `*` | Comma-separated allowed origins for CORS |

## Running Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`.
