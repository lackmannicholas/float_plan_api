from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_float_plans.db"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


SAMPLE_PLAN = {
    "submitter_name": "Jane Smith",
    "submitter_phone": "555-0100",
    "submitter_email": "jane@example.com",
    "vessel_name": "Sea Breeze",
    "vessel_type": "Sailboat",
    "vessel_registration": "FL-1234-AB",
    "vessel_length_ft": 28,
    "vessel_color": "White",
    "vessel_engine_count": 1,
    "vessel_fuel_type": "Diesel",
    "departure_location": "Marina Bay",
    "destination": "Island Cove",
    "departure_time": "2025-07-04T09:00:00",
    "expected_return_time": "2025-07-04T18:00:00",
    "route_description": "Head south along the coast.",
    "flares": True,
    "life_jackets_count": 4,
    "epirb": True,
    "vhf_radio": True,
    "cell_phone": "555-0101",
    "emergency_notes": "Call coast guard if not back by 19:00.",
    "passengers": [
        {"name": "Bob Smith", "age": 45, "swim_ability": "strong"},
        {"name": "Alice Smith", "age": 12, "swim_ability": "moderate"},
    ],
    "emergency_contacts": [
        {
            "name": "Carol Smith",
            "phone": "555-0102",
            "contact_relationship": "Sister",
            "notify_if_overdue": True,
        }
    ],
}


class TestHealthCheck:
    def test_root(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestCreateFloatPlan:
    def test_create_float_plan(self, client):
        response = client.post("/float_plans/", json=SAMPLE_PLAN)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["vessel_name"] == "Sea Breeze"
        assert data["submitter_name"] == "Jane Smith"
        assert len(data["passengers"]) == 2
        assert len(data["emergency_contacts"]) == 1
        assert data["passengers"][0]["name"] == "Bob Smith"
        assert data["emergency_contacts"][0]["name"] == "Carol Smith"

    def test_create_float_plan_minimal(self, client):
        minimal_plan = {
            "submitter_name": "Tom",
            "submitter_phone": "555-0200",
            "vessel_name": "Tiny Boat",
            "vessel_type": "Dinghy",
            "departure_location": "Dock A",
            "destination": "Dock B",
            "departure_time": "2025-08-01T10:00:00",
            "expected_return_time": "2025-08-01T12:00:00",
        }
        response = client.post("/float_plans/", json=minimal_plan)
        assert response.status_code == 201
        data = response.json()
        assert data["vessel_name"] == "Tiny Boat"
        assert data["passengers"] == []
        assert data["emergency_contacts"] == []

    def test_create_float_plan_missing_required_field(self, client):
        incomplete_plan = {k: v for k, v in SAMPLE_PLAN.items() if k != "vessel_name"}
        response = client.post("/float_plans/", json=incomplete_plan)
        assert response.status_code == 422


class TestGetFloatPlan:
    def test_get_float_plan(self, client):
        client.post("/float_plans/", json=SAMPLE_PLAN)
        response = client.get("/float_plans/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["vessel_name"] == "Sea Breeze"

    def test_get_float_plan_not_found(self, client):
        response = client.get("/float_plans/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Float plan not found"


class TestListFloatPlans:
    def test_list_float_plans_empty(self, client):
        response = client.get("/float_plans/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_float_plans(self, client):
        client.post("/float_plans/", json=SAMPLE_PLAN)
        second_plan = {**SAMPLE_PLAN, "vessel_name": "Wind Dancer"}
        client.post("/float_plans/", json=second_plan)
        response = client.get("/float_plans/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["vessel_name"] == "Sea Breeze"
        assert data[1]["vessel_name"] == "Wind Dancer"

    def test_list_float_plans_pagination(self, client):
        for i in range(5):
            plan = {**SAMPLE_PLAN, "vessel_name": f"Boat {i}"}
            client.post("/float_plans/", json=plan)
        response = client.get("/float_plans/?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2


class TestUpdateFloatPlan:
    def test_update_float_plan(self, client):
        client.post("/float_plans/", json=SAMPLE_PLAN)
        update_data = {"vessel_name": "Updated Vessel", "vessel_type": "Motorboat"}
        response = client.put("/float_plans/1", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["vessel_name"] == "Updated Vessel"
        assert data["vessel_type"] == "Motorboat"

    def test_update_float_plan_passengers(self, client):
        client.post("/float_plans/", json=SAMPLE_PLAN)
        update_data = {
            "passengers": [{"name": "New Passenger", "age": 30, "swim_ability": "good"}]
        }
        response = client.put("/float_plans/1", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert len(data["passengers"]) == 1
        assert data["passengers"][0]["name"] == "New Passenger"

    def test_update_float_plan_not_found(self, client):
        update_data = {"vessel_name": "Ghost Vessel"}
        response = client.put("/float_plans/999", json=update_data)
        assert response.status_code == 404


class TestDeleteFloatPlan:
    def test_delete_float_plan(self, client):
        client.post("/float_plans/", json=SAMPLE_PLAN)
        response = client.delete("/float_plans/1")
        assert response.status_code == 204
        # Verify it's gone
        get_response = client.get("/float_plans/1")
        assert get_response.status_code == 404

    def test_delete_float_plan_not_found(self, client):
        response = client.delete("/float_plans/999")
        assert response.status_code == 404
