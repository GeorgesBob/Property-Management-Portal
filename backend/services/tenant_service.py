# service/tenant_service.py
from sqlalchemy.orm import Session
from utils.helper_functions import validate_tenant_data
from repository.tenant_repository import (create_tenant as repo_create_tenant, 
get_tenant_by_id as repo_get_tenant_by_id, 
get_all_tenants as repo_get_all_tenants, 
update_tenant as repo_update_tenant, 
delete_tenant as repo_delete_tenant)
from utils.helper_functions import serialize_sqlalchemy_objects, serialize_object

def get_all_tenants(db:Session):
    return serialize_sqlalchemy_objects(repo_get_all_tenants(db))

def get_tenant_by_id(db: Session, tenant_id: int):
    return serialize_object(repo_get_tenant_by_id(db, tenant_id))

def create_tenant(db: Session, tenant_data: dict):
    if not validate_tenant_data(tenant_data):
        raise ValueError("Invalid tenant data")
    return repo_create_tenant(db,tenant_data)

def update_tenant(db: Session, tenant_id: int, updates: dict):
    if not validate_tenant_data(updates):
        raise ValueError("Invalid updates data")
    return repo_create_tenant(db,tenant_id,updates)

def delete_tenant(db:Session, tenant_id:int):
    return repo_delete_tenant(db,tenant_id)

