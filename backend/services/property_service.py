# service/property_service.py
from sqlalchemy.orm import Session
from utils.helper_functions import validate_property_data
from repository.property_repository import (create_property as repo_create_property, 
get_property_by_id as repo_get_property_by_id, 
get_all_properties as repo_get_all_properties, 
update_property as repo_update_property, 
delete_property as repo_delete_property)
from utils.helper_functions import serialize_sqlalchemy_objects, serialize_object

def get_all_properties(db:Session):
    return serialize_sqlalchemy_objects(repo_get_all_properties(db))

def get_property_by_id(db: Session, property_id: int):
    return serialize_object(repo_get_property_by_id(db, property_id))

def create_property(db: Session, property_data: dict):
    if not validate_property_data(property_data):
        raise ValueError("Invalid property data")
    return repo_create_property(db, property_data)

def update_property(db: Session, property_id: int, updates: dict):
    if not validate_property_data(updates):
        raise ValueError("Invalid updates data")
    return repo_update_property(db,property_id, updates)

def delete_property(db:Session, property_id:int):
    return repo_delete_property(db,property_id)

