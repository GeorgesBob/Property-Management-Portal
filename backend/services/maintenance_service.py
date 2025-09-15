# service/maintenance_service.py
from sqlalchemy.orm import Session
from utils.helper_functions import validate_maintenance_data
from repository.maintenance_repository import (create_maintenance as repo_create_maintenance, 
get_maintenance_by_id as repo_get_maintenance_by_id, 
get_all_maintenances as repo_get_all_maintenances, 
update_maintenance as repo_update_maintenance, 
delete_maintenance as repo_delete_maintenance)
from utils.helper_functions import serialize_sqlalchemy_objects, serialize_object

def get_all_maintenances(db:Session):
    return serialize_sqlalchemy_objects(repo_get_all_maintenances(db))

def get_maintenance_by_id(db: Session, maintenance_id: int):
    return serialize_object(repo_get_maintenance_by_id(db, maintenance_id))

def create_maintenance(db: Session, maintenance_data: dict):
    if not validate_maintenance_data(maintenance_data):
        raise ValueError("Invalid maintenance data")
    return repo_create_maintenance(db, maintenance_data)

def update_maintenance(db: Session, maintenance_id: int, updates: dict):
    if not validate_maintenance_data(updates):
        raise ValueError("Invalid updates data")
    return repo_update_maintenance(db,maintenance_id, updates)

def delete_maintenance(db:Session, maintenance_id:int):
    return repo_delete_maintenance(db,maintenance_id)

