import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---- GET ALL ----
def test_get_all_properties(client, monkeypatch):
    def fake_get_all_properties(db):
        return [{
            "PropertyID": 1,
            "Address": "8 Avenue Foch, Lyon, 69006",
            "Price": 950000,
            "PropertyType": "Commercial",
            "PurchaseDate": "2019-11-30",
            "Status": "Occupied"
        }]

    monkeypatch.setattr(
        "controllers.property_controller.service_get_all_properties",
        fake_get_all_properties
    )

    response = client.get("/property/")
    assert response.status_code == 200
    assert response.get_json()[0]["Address"] == "8 Avenue Foch, Lyon, 69006"


# ---- GET BY ID ----
def test_get_property_by_id(client, monkeypatch):
    def fake_get_property_by_id(db, property_id):
        return {
            "PropertyID": property_id,
            "Address": "8 Avenue Foch, Lyon, 69006",
            "Price": 950000,
            "PropertyType": "Commercial",
            "PurchaseDate": "2019-11-30",
            "Status": "Occupied"
        }

    monkeypatch.setattr(
        "controllers.property_controller.service_get_property_by_id",
        fake_get_property_by_id
    )

    response = client.get("/property/123")
    assert response.status_code == 200
    assert response.get_json()["PropertyID"] == 123


# ---- CREATE ----
def test_create_property(client, monkeypatch):
    def fake_create_property(db, data):
        return {"PropertyID": 10, **data}

    monkeypatch.setattr(
        "controllers.property_controller.service_create_property",
        fake_create_property
    )

    response = client.post("/property/", json={
        "Address": "8 Avenue Foch, Lyon, 69006",
        "Price": 950000,
        "PropertyType": "Commercial",
        "PurchaseDate": "2019-11-30",
        "Status": "Occupied"
    })
    assert response.status_code == 201
    assert response.get_json()["status"] == "OK"


# ---- UPDATE ----
def test_update_property(client, monkeypatch):
    def fake_update_property(db, property_id, data):
        return {"PropertyID": property_id, **data}

    monkeypatch.setattr(
        "controllers.property_controller.service_update_property",
        fake_update_property
    )

    response = client.patch("/property/1", json={"Status": "Vacant"})
    assert response.status_code == 200
    assert response.get_json()["status"] == "OK"


# ---- DELETE ----
def test_delete_property(client, monkeypatch):
    def fake_delete_property(db, property_id):
        return True

    monkeypatch.setattr(
        "controllers.property_controller.service_delete_property",
        fake_delete_property
    )

    response = client.delete("/property/1")
    assert response.status_code == 200
    assert response.get_json()["status"] == "Delete"
