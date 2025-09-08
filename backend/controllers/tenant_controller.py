from flask import Blueprint, jsonify
from services.tenant_service import (
    get_all_tenants as service_get_all_tenants,
    get_tenant_by_id as service_get_tenant_by_id,
    create_tenant    as service_create_tenant,
    update_tenant as service_update_tenant
)
from models.base import SessionLocal

tenant_bp = Blueprint("tenant", __name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@tenant_bp.route('/', methods=["GET"])
def get_all_tenants():
    db = next(get_db())
    tenants = service_get_all_tenants(db)
    if not tenants:
        return jsonify([]), 200  # return empty list instead of 404
    return jsonify(tenants), 200

@tenant_bp.route('/<int:tenant_id>', methods=["GET"])
def get_tenant(tenant_id):
    db = next(get_db())
    tenant = service_get_tenant_by_id(db, tenant_id)
    if not tenant:
        return jsonify({"error": "tenant not found"}), 404
    return jsonify(tenant), 200
@tenant_bp.route("/", methods=["POST"])
def create_tenant():
    try:
        data = request.get_json()
        ten = service_create_tenant(db, data)
        if not ten:
            return jsonify({"error": "tenant not found"}), 404
        return jsonify({"status": "Valid"}), 200,
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400    

@tenant_bp.route('/<int:tenant_id>', methods=["PATCH"])
def update_tenant(tenant_id):
    try:
        data = request.get_json()
        ten = service_update_tenant(db, tenant_id, data)
        if not ten:
            return jsonify({"error": "tenant not found"}), 404
        return jsonify({"status": "Valid"}), 200,
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400    





