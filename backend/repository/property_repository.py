from sqlalchemy.orm import Session
from models.property import Property
from sqlalchemy.exc import SQLAlchemyError

def create_property(db: Session, propertyData: dict):
    try:
        property_obj = Property(**propertyData)
        db.add(property_obj)
        db.commit()
        db.refresh(property_obj)
        return property_obj
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def get_all_properties(db: Session):
    try:
        return db.query(Property).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def get_property_by_id(db: Session, property_id: int):
    try:
        return db.get(Property, property_id)
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def update_property(db: Session, property_id: int, updates: dict):
    try:
        property_obj = db.get(Property, property_id)
        if not property_obj:
            return None  # ou raise ValueError(f"Property {property_id} not found")

        for key, value in updates.items():
            if hasattr(property_obj, key):
                setattr(property_obj, key, value)

        db.commit()
        db.refresh(property_obj)
        return property_obj
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def delete_property(db: Session, property_id: int):
    try:
        property_obj = db.get(Property, property_id)
        if property_obj:
            db.delete(property_obj)
            db.commit()
        return property_obj
    except SQLAlchemyError as e:
        db.rollback()
        raise e
