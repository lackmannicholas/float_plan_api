import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import float_plans

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Float Plan API",
    description="REST API backend for the float_plan frontend application. "
    "Allows boaters to create and manage float plans for safe on-water travel.",
    version="1.0.0",
)

_cors_origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "*")
cors_origins: list[str] | str = (
    [origin.strip() for origin in _cors_origins_env.split(",")]
    if _cors_origins_env != "*"
    else ["*"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(float_plans.router)


@app.get("/", tags=["health"])
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Float Plan API is running"}
