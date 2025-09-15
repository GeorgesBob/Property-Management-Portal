import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---- GET ALL ----
def test_get_all_maintenances(client, monkeypatch):
    def fake_get_all_maintenances(db):
        return [{
            "Status": "In Progress",
            "Description": "Repaint exterior walls",
            "PropertyID": 3,
            "ScheduledDate": "2025-09-19",
            "MaintenanceID": 1
        }]

    monkeypatch.setattr(
        "controllers.maintenance_controller.service_get_all_maintenances",
        fake_get_all_maintenances
    )

    response = client.get("/maintenance/")
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]["Status"] == "In Progress"
    assert data[0]["Description"] == "Repaint exterior walls"


# ---- GET BY ID ----
def test_get_maintenance_by_id(client, monkeypatch):
    def fake_get_maintenance_by_id(db, maintenance_id):
        return {
            "Status": "In Progress",
            "Description": "Repaint exterior walls",
            "PropertyID": 3,
            "ScheduledDate": "2025-09-19",
            "MaintenanceID": maintenance_id
        }

    monkeypatch.setattr(
        "controllers.maintenance_controller.service_get_maintenance_by_id",
        fake_get_maintenance_by_id
    )

    response = client.get("/maintenance/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["MaintenanceID"] == 1
    assert data["Status"] == "In Progress"


# ---- CREATE ----
def test_create_maintenance(client, monkeypatch):
    def fake_create_maintenance(db, data):
        return {**data, "MaintenanceID": 2}

    monkeypatch.setattr(
        "controllers.maintenance_controller.service_create_maintenance",
        fake_create_maintenance
    )

    payload = {
        "Status": "In Progress",
        "Description": "Repaint exterior walls",
        "PropertyID": 3,
        "ScheduledDate": "2025-09-19"
    }

    response = client.post("/maintenance/", json=payload)
    assert response.status_code == 201
    assert response.get_json()["status"] in ["Create", "OK"]


# ---- UPDATE ----
def test_update_maintenance(client, monkeypatch):
    def fake_update_maintenance(db, maintenance_id, data):
        return {**data, "MaintenanceID": maintenance_id}

    monkeypatch.setattr(
        "controllers.maintenance_controller.service_update_maintenance",
        fake_update_maintenance
    )

    response = client.patch("/maintenance/1", json={"Status": "Completed"})
    assert response.status_code in [200, 201]
    assert response.get_json()["status"] in ["Update", "OK"]


# ---- DELETE ----
def test_delete_maintenance(client, monkeypatch):
    def fake_delete_maintenance(db, maintenance_id):
        return True

    monkeypatch.setattr(
        "controllers.maintenance_controller.service_delete_maintenance",
        fake_delete_maintenance
    )

    response = client.delete("/maintenance/1")
    assert response.status_code == 200
    assert response.get_json()["status"] in ["Delete"]
