from flask import Blueprint, jsonify
from services.maintenance_service import (get_all_maintenances as service_get_all_maintenances, get_maintenance_by_id as service_get_maintenance_by_id)
from models.base import SessionLocal

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