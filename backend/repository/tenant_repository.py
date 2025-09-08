from sqlalchemy.orm import Session
from models.tenant import Tenant
from sqlalchemy.exc import SQLAlchemyError

def create_tenant(db: Session, tenantData: dict):
    try:
        tenant_obj = Tenant(**tenantData)
        db.add(tenant_obj)
        db.commit()
        db.refresh(tenant_obj)
        return tenant_obj
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def get_all_tenants(db: Session):
    try:
        return db.query(Tenant).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def get_tenant_by_id(db: Session, tenant_id: int):
    try:
        return db.get(Tenant, tenant_id)
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def update_tenant(db: Session, tenant_id: int, updates: dict):
    try:
        tenant_obj = db.get(Tenant, tenant_id)
        if not tenant_obj:
            return None  # ou raise ValueError(f"tenant {tenant_id} not found")

        for key, value in updates.items():
            if hasattr(tenant_obj, key):
                setattr(tenant_obj, key, value)

        db.commit()
        db.refresh(tenant_obj)
        return tenant_obj
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def delete_tenant(db: Session, tenant_id: int):
    try:
        tenant_obj = db.get(tenant, tenant_id)
        if tenant_obj:
            db.delete(tenant_obj)
            db.commit()
        return tenant_obj
    except SQLAlchemyError as e:
        db.rollback()
        raise e
