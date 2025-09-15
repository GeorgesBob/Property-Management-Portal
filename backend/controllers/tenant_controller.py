from flask import Blueprint,request, jsonify
from pydantic import ValidationError
from services.tenant_service import (
    get_all_tenants as service_get_all_tenants,
    get_tenant_by_id as service_get_tenant_by_id,
    create_tenant    as service_create_tenant,
    update_tenant as service_update_tenant,
    delete_tenant as service_delete_tenant
)
from models.base import SessionLocal

tenant_bp = Blueprint("tenant", __name__)

db = SessionLocal()

# get all tenants 
@tenant_bp.route('/', methods=["GET"])
def get_all_tenants():
    tenants = service_get_all_tenants(db)
    if not tenants:
        return jsonify({"error": "tenants not found"}), 404
    return jsonify(tenants), 200

# get one tenant 

@tenant_bp.route('/<int:tenant_id>', methods=["GET"])
def get_tenant(tenant_id):
    tenant = service_get_tenant_by_id(db, tenant_id)
    if tenant == None:
        return jsonify({"error": "tenant not found"}), 404
    return jsonify(tenant), 200
@tenant_bp.route("/", methods=["POST"])

# create tenant
def create_tenant():
    try:
        data = request.get_json()
        ten = service_create_tenant(db, data)
        if not ten:
            return jsonify({"error": "tenant not found"}), 404
        return jsonify({"status": "Create"}), 200,
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400    

# Update tenant
@tenant_bp.route('/<int:tenant_id>', methods=["PATCH"])
def update_tenant(tenant_id):
    try:
        data = request.get_json()
        ten = service_update_tenant(db, tenant_id, data)
        if not ten:
            return jsonify({"error": "tenant not found"}), 404
        return jsonify({"status": "Update"}), 201,
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400 

#Update Tenant
@tenant_bp.route('/<int:tenant_id>', methods=["DELETE"])
def delete_tenant(tenant_id):
    try:
        ten = service_delete_tenant(db, tenant_id)
        if not ten:
            return jsonify({"error": "tenant not found"}), 404
        return jsonify({"status": "Delete"}), 200,
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400    



