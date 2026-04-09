from sqlalchemy.orm import Session

from app import models, schemas


def get_float_plan(db: Session, float_plan_id: int) -> models.FloatPlan | None:
    return (
        db.query(models.FloatPlan).filter(models.FloatPlan.id == float_plan_id).first()
    )


def get_float_plans(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.FloatPlan]:
    return db.query(models.FloatPlan).offset(skip).limit(limit).all()


def create_float_plan(
    db: Session, float_plan: schemas.FloatPlanCreate
) -> models.FloatPlan:
    passengers_data = float_plan.passengers
    contacts_data = float_plan.emergency_contacts

    plan_data = float_plan.model_dump(exclude={"passengers", "emergency_contacts"})
    db_plan = models.FloatPlan(**plan_data)

    for p in passengers_data:
        db_plan.passengers.append(models.Passenger(**p.model_dump()))

    for c in contacts_data:
        db_plan.emergency_contacts.append(models.EmergencyContact(**c.model_dump()))

    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


def update_float_plan(
    db: Session, float_plan_id: int, float_plan: schemas.FloatPlanUpdate
) -> models.FloatPlan | None:
    db_plan = get_float_plan(db, float_plan_id)
    if db_plan is None:
        return None

    update_data = float_plan.model_dump(
        exclude_unset=True, exclude={"passengers", "emergency_contacts"}
    )
    for field, value in update_data.items():
        setattr(db_plan, field, value)

    if float_plan.passengers is not None:
        for passenger in db_plan.passengers:
            db.delete(passenger)
        db_plan.passengers = [
            models.Passenger(**p.model_dump()) for p in float_plan.passengers
        ]

    if float_plan.emergency_contacts is not None:
        for contact in db_plan.emergency_contacts:
            db.delete(contact)
        db_plan.emergency_contacts = [
            models.EmergencyContact(**c.model_dump())
            for c in float_plan.emergency_contacts
        ]

    db.commit()
    db.refresh(db_plan)
    return db_plan


def delete_float_plan(db: Session, float_plan_id: int) -> bool:
    db_plan = get_float_plan(db, float_plan_id)
    if db_plan is None:
        return False
    db.delete(db_plan)
    db.commit()
    return True
