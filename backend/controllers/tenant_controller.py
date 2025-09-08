from flask import Blueprint, jsonify
from services.tenant_service import (get_all_tenants as service_get_all_tenants, get_tenant_by_id as service_get_tenant_by_id)
from models.base import SessionLocal

tenant_bp = Blueprint("tenant", __name__)
db = SessionLocal()

@tenant_bp.route('/')
def get_all_tenants():
    tenants = service_get_all_tenants(db)
    if not tenants:
        return jsonify({"error": "tenants not found"}), 404
    return jsonify(tenants), 200

@tenant_bp.route('/<int:tenant_id>')
def get_tenant(tenant_id):
    tenant = service_get_tenant_by_id(db, tenant_id)
    if not tenant:
        return jsonify({"error": "tenant not found"}), 404
    return jsonify(tenant), 200






