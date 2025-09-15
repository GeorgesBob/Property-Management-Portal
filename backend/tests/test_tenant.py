import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---- GET ALL ----
def test_get_all_tenants(client, monkeypatch):
    def fake_get_all_tenants(db):
        return [{
            "ContactInfo": "+33456789012",
            "LeaseTermEnd": "2024-01-14",
            "LeaseTermStart": "2023-01-15",
            "Name": "Marie Curie",
            "PropertyID": 2,
            "RentalPaymentStatus": "Pending",
            "TenantID": 2
        }]

    monkeypatch.setattr(
        "controllers.tenant_controller.service_get_all_tenants",
        fake_get_all_tenants
    )

    response = client.get("/tenant/")
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]["Name"] == "Marie Curie"
    assert data[0]["RentalPaymentStatus"] == "Pending"


# ---- GET BY ID ----
def test_get_tenant_by_id(client, monkeypatch):
    def fake_get_tenant_by_id(db, tenant_id):
        return {
            "ContactInfo": "+33456789012",
            "LeaseTermEnd": "2024-01-14",
            "LeaseTermStart": "2023-01-15",
            "Name": "Marie Curie",
            "PropertyID": 2,
            "RentalPaymentStatus": "Pending",
            "TenantID": tenant_id
        }

    monkeypatch.setattr(
        "controllers.tenant_controller.service_get_tenant_by_id",
        fake_get_tenant_by_id
    )

    response = client.get("/tenant/2")
    assert response.status_code == 200
    data = response.get_json()
    assert data["TenantID"] == 2
    assert data["Name"] == "Marie Curie"


# ---- CREATE ----
def test_create_tenant(client, monkeypatch):
    def fake_create_tenant(db, data):
        return {**data, "TenantID": 2}

    monkeypatch.setattr(
        "controllers.tenant_controller.service_create_tenant",
        fake_create_tenant
    )

    payload = {
        "ContactInfo": "+33456789012",
        "LeaseTermEnd": "2024-01-14",
        "LeaseTermStart": "2023-01-15",
        "Name": "Marie Curie",
        "PropertyID": 2,
        "RentalPaymentStatus": "Pending"
    }

    response = client.post("/tenant/", json=payload)
    assert response.status_code == 200
    assert response.get_json()["status"] == "Create"


# ---- UPDATE ----
def test_update_tenant(client, monkeypatch):
    def fake_update_tenant(db, tenant_id, data):
        return {**data, "TenantID": tenant_id}

    monkeypatch.setattr(
        "controllers.tenant_controller.service_update_tenant",
        fake_update_tenant
    )

    response = client.patch("/tenant/2", json={"RentalPaymentStatus": "Paid"})
    assert response.status_code == 201
    assert response.get_json()["status"] == "Update"


# ---- DELETE ----
def test_delete_tenant(client, monkeypatch):
    def fake_delete_tenant(db, tenant_id):
        return True

    monkeypatch.setattr(
        "controllers.tenant_controller.service_delete_tenant",
        fake_delete_tenant
    )

    response = client.delete("/tenant/2")
    assert response.status_code == 200
    assert response.get_json()["status"] == "Delete"
