from repository.property_repository import get_all_properties, get_property_by_id # ton fichier où sont tes fonctions
from repository.tenant_repository import get_all_tenants, get_tenant_by_id
from repository.maintenance_repository import get_all_maintenances, get_maintenance_by_id
from services.property_service import (get_all_properties as service_get_all_property,
get_property_by_id as service_get_property_by_id, create_property as service_create_property)
from utils.helper_functions import serialize_sqlalchemy_objects
from models.base import SessionLocal

db = SessionLocal()

data = {
    "Address": "3 Quai de Grenelle, Marseille, 13002",
    "PropertyType": "Residential",
    "Status": "Occupied",
    "PurchaseDate":"2020-06-15",
    "Price":"2000"
}
print("Create property")
create_property = service_create_property(db,data)
print(create_property)