from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class PassengerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    age: int | None = Field(None, ge=0, le=150)
    swim_ability: str | None = Field(None, max_length=50)


class PassengerCreate(PassengerBase):
    pass


class PassengerRead(PassengerBase):
    id: int

    model_config = {"from_attributes": True}


class EmergencyContactBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    phone: str = Field(..., min_length=7, max_length=50)
    contact_relationship: str | None = Field(None, max_length=100)
    notify_if_overdue: bool = True


class EmergencyContactCreate(EmergencyContactBase):
    pass


class EmergencyContactRead(EmergencyContactBase):
    id: int

    model_config = {"from_attributes": True}


class FloatPlanBase(BaseModel):
    # Submitter info
    submitter_name: str = Field(..., min_length=1, max_length=255)
    submitter_phone: str = Field(..., min_length=7, max_length=50)
    submitter_email: str | None = Field(None, max_length=255)

    # Vessel info
    vessel_name: str = Field(..., min_length=1, max_length=255)
    vessel_type: str = Field(..., min_length=1, max_length=100)
    vessel_registration: str | None = Field(None, max_length=100)
    vessel_length_ft: int | None = Field(None, ge=1, le=1000)
    vessel_color: str | None = Field(None, max_length=100)
    vessel_engine_count: int | None = Field(None, ge=0, le=20)
    vessel_fuel_type: str | None = Field(None, max_length=50)

    # Trip details
    departure_location: str = Field(..., min_length=1, max_length=255)
    destination: str = Field(..., min_length=1, max_length=255)
    departure_time: datetime
    expected_return_time: datetime
    route_description: str | None = None

    # Safety equipment
    flares: bool | None = None
    life_jackets_count: int | None = Field(None, ge=0)
    epirb: bool | None = None
    vhf_radio: bool | None = None
    cell_phone: str | None = Field(None, max_length=50)
    emergency_notes: str | None = None


class FloatPlanCreate(FloatPlanBase):
    passengers: list[PassengerCreate] = []
    emergency_contacts: list[EmergencyContactCreate] = []


class FloatPlanUpdate(FloatPlanBase):
    submitter_name: str | None = Field(None, min_length=1, max_length=255)
    submitter_phone: str | None = Field(None, min_length=7, max_length=50)
    vessel_name: str | None = Field(None, min_length=1, max_length=255)
    vessel_type: str | None = Field(None, min_length=1, max_length=100)
    departure_location: str | None = Field(None, min_length=1, max_length=255)
    destination: str | None = Field(None, min_length=1, max_length=255)
    departure_time: datetime | None = None
    expected_return_time: datetime | None = None
    passengers: list[PassengerCreate] | None = None
    emergency_contacts: list[EmergencyContactCreate] | None = None


class FloatPlanRead(FloatPlanBase):
    id: int
    created_at: datetime
    updated_at: datetime
    passengers: list[PassengerRead] = []
    emergency_contacts: list[EmergencyContactRead] = []

    model_config = {"from_attributes": True}


class FloatPlanSummary(BaseModel):
    id: int
    submitter_name: str
    vessel_name: str
    departure_location: str
    destination: str
    departure_time: datetime
    expected_return_time: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
