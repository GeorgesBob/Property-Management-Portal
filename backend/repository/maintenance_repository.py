from sqlalchemy.orm import Session
from models.maintenance import Maintenance
from sqlalchemy.exc import SQLAlchemyError

def create_maintenance(db: Session, maintenanceData: dict):
    try:
        maintenance_obj = Maintenance(**maintenanceData)
        db.add(maintenance_obj)
        db.commit()
        db.refresh(maintenance_obj)
        return maintenance_obj
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def get_all_maintenances(db: Session):
    try:
        return db.query(Maintenance).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def get_maintenance_by_id(db: Session, maintenance_id: int):
    try:
        return db.get(Maintenance, maintenance_id)
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def update_maintenance(db: Session, maintenance_id: int, updates: dict):
    try:
        maintenance_obj = db.get(Maintenance, maintenance_id)
        if not maintenance_obj:
            return None  # ou raise ValueError(f"maintenance {maintenance_id} not found")

        for key, value in updates.items():
            if hasattr(maintenance_obj, key):
                setattr(maintenance_obj, key, value)

        db.commit()
        db.refresh(maintenance_obj)
        return maintenance_obj
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def delete_maintenance(db: Session, maintenance_id: int):
    try:
        maintenance_obj = db.get(Maintenance, maintenance_id)
        if maintenance_obj:
            db.delete(maintenance_obj)
            db.commit()
        return maintenance_obj
    except SQLAlchemyError as e:
        db.rollback()
        raise e
