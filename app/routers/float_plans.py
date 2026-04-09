from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/float_plans", tags=["float_plans"])


@router.get("/", response_model=list[schemas.FloatPlanSummary])
def list_float_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """List all float plans (summary view)."""
    return crud.get_float_plans(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.FloatPlanRead, status_code=201)
def create_float_plan(
    float_plan: schemas.FloatPlanCreate,
    db: Session = Depends(get_db),
):
    """Create a new float plan."""
    return crud.create_float_plan(db, float_plan)


@router.get("/{float_plan_id}", response_model=schemas.FloatPlanRead)
def get_float_plan(
    float_plan_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific float plan by ID."""
    plan = crud.get_float_plan(db, float_plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Float plan not found")
    return plan


@router.put("/{float_plan_id}", response_model=schemas.FloatPlanRead)
def update_float_plan(
    float_plan_id: int,
    float_plan: schemas.FloatPlanUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing float plan."""
    updated = crud.update_float_plan(db, float_plan_id, float_plan)
    if updated is None:
        raise HTTPException(status_code=404, detail="Float plan not found")
    return updated


@router.delete("/{float_plan_id}", status_code=204)
def delete_float_plan(
    float_plan_id: int,
    db: Session = Depends(get_db),
):
    """Delete a float plan."""
    deleted = crud.delete_float_plan(db, float_plan_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Float plan not found")
