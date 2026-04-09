from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class FloatPlan(Base):
    __tablename__ = "float_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # Submitter info
    submitter_name: Mapped[str] = mapped_column(String(255))
    submitter_phone: Mapped[str] = mapped_column(String(50))
    submitter_email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Vessel info
    vessel_name: Mapped[str] = mapped_column(String(255))
    vessel_type: Mapped[str] = mapped_column(String(100))
    vessel_registration: Mapped[str | None] = mapped_column(String(100), nullable=True)
    vessel_length_ft: Mapped[int | None] = mapped_column(Integer, nullable=True)
    vessel_color: Mapped[str | None] = mapped_column(String(100), nullable=True)
    vessel_engine_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    vessel_fuel_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Trip details
    departure_location: Mapped[str] = mapped_column(String(255))
    destination: Mapped[str] = mapped_column(String(255))
    departure_time: Mapped[datetime] = mapped_column(DateTime)
    expected_return_time: Mapped[datetime] = mapped_column(DateTime)
    route_description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Safety equipment
    flares: Mapped[bool | None] = mapped_column(nullable=True)
    life_jackets_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    epirb: Mapped[bool | None] = mapped_column(nullable=True)
    vhf_radio: Mapped[bool | None] = mapped_column(nullable=True)
    cell_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    emergency_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=_utcnow, onupdate=_utcnow
    )

    passengers: Mapped[list["Passenger"]] = relationship(
        "Passenger", back_populates="float_plan", cascade="all, delete-orphan"
    )
    emergency_contacts: Mapped[list["EmergencyContact"]] = relationship(
        "EmergencyContact", back_populates="float_plan", cascade="all, delete-orphan"
    )


class Passenger(Base):
    __tablename__ = "passengers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    float_plan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("float_plans.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255))
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    swim_ability: Mapped[str | None] = mapped_column(String(50), nullable=True)

    float_plan: Mapped["FloatPlan"] = relationship(
        "FloatPlan", back_populates="passengers"
    )


class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    float_plan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("float_plans.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(50))
    contact_relationship: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notify_if_overdue: Mapped[bool] = mapped_column(default=True)

    float_plan: Mapped["FloatPlan"] = relationship(
        "FloatPlan", back_populates="emergency_contacts"
    )
