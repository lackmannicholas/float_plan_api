# float_plan_api
Float Plan API backend

## Overview

A FastAPI backend for the [float_plan](https://github.com/lackmannicholas/float_plan) frontend. Boaters use this API to create, store, and manage float plans — safety documents left with someone before heading out on the water.

## Features

- Full CRUD operations for float plans
- Passenger and emergency contact management per plan
- SQLite database via SQLAlchemy ORM
- Automatic OpenAPI docs at `/docs`
- CORS enabled for frontend integration

## Project Structure

```
float_plan_api/
├── app/
│   ├── main.py          # FastAPI app & middleware
│   ├── database.py      # SQLAlchemy engine & session
│   ├── models.py        # ORM models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── crud.py          # Database operations
│   └── routers/
│       └── float_plans.py  # API routes
├── tests/
│   └── test_float_plans.py
└── requirements.txt
```

## Getting Started

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

## Configuration

| Environment Variable | Default | Description |
|---|---|---|
| `CORS_ALLOWED_ORIGINS` | `*` | Comma-separated list of allowed origins (e.g. `https://example.com,https://app.example.com`). Defaults to `*` (all origins) for local development. |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/float_plans/` | List all float plans |
| POST | `/float_plans/` | Create a new float plan |
| GET | `/float_plans/{id}` | Get a float plan |
| PUT | `/float_plans/{id}` | Update a float plan |
| DELETE | `/float_plans/{id}` | Delete a float plan |

## Running Tests

```bash
pytest tests/ -v
```
