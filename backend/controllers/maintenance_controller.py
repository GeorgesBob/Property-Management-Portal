from flask import Blueprint,request, jsonify
from services.maintenance_service import (get_all_maintenances as service_get_all_maintenances, get_maintenance_by_id as service_get_maintenance_by_id, update_maintenance as service_update_maintenance, create_maintenance as service_create_maintenance)
from models.base import SessionLocal
from pydantic import ValidationError
maintenance_bp = Blueprint("maintenance", __name__)
db = SessionLocal()

@maintenance_bp.route('/')
def get_all_maintenances():
    maintenances = service_get_all_maintenances(db)
    if not maintenances:
        return jsonify({"error": "maintenances not found"}), 404
    return jsonify(maintenances), 200

@maintenance_bp.route('/<int:maintenance_id>')
def get_maintenance(maintenance_id):
    maintenance = service_get_maintenance_by_id(db, maintenance_id)
    if not maintenance: 
        return jsonify({"error": "maintenance not found"}), 404
    return jsonify(maintenance), 200

@maintenance_bp.route("/", methods=["POST"])
def create_maintenance():
    try:
        data = request.get_json()
        maintenance = service_create_maintenance(db, data)

        if not maintenance:
            return jsonify({"error": "Maintenance not created"}), 400

        # ✅ si tout va bien
        return jsonify({"status": "OK"}), 201,

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
   

@maintenance_bp.route('/<int:maintenance_id>', methods=["PATCH"])
def update_maintenance(maintenance_id):
    try:
        data = request.get_json()
        maintenance = service_update_maintenance(db, maintenance_id, data)
        if not maintenance:
            return jsonify({"error": "maintenance not found"}), 404
        return jsonify(maintenance), 200
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400    





