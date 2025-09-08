from flask import Blueprint,request, jsonify
from services.property_service import (get_all_properties as service_get_all_properties, get_property_by_id as service_get_property_by_id, update_property as service_update_property, create_property as service_create_property)
from models.base import SessionLocal
from pydantic import ValidationError
property_bp = Blueprint("property", __name__)
db = SessionLocal()

@property_bp.route('/')
def get_all_properties():
    properties = service_get_all_properties(db)
    if not property:
        return jsonify({"error": "proeprties not found"}), 404
    return jsonify(properties), 200

@property_bp.route('/<int:property_id>')
def get_property(property_id):
    prop = service_get_property_by_id(db, property_id)
    if not prop: 
        return jsonify({"error": "property not found"}), 404
    return jsonify(prop), 200

@property_bp.route("/", methods=["POST"])
def create_property():
    try:
        data = request.get_json()
        prop = service_create_property(db, data)

        if not prop:
            return jsonify({"error": "property not found"}), 404
        return jsonify({"status": "OK"}), 200
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400   

@property_bp.route('/<int:property_id>', methods=["PATCH"])
def update_property(property_id):
    try:
        data = request.get_json()
        prop = service_update_property(db, property_id, data)
        if not prop:
            return jsonify({"error": "property not found"}), 404
        return jsonify({"status": "OK"}), 200,
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400    





