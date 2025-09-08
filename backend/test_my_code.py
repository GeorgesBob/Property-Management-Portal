from repository.property_repository import get_all_properties, get_property_by_id # ton fichier où sont tes fonctions
from repository.tenant_repository import get_all_tenants, get_tenant_by_id
from repository.maintenance_repository import get_all_maintenances, get_maintenance_by_id
from services.property_service import (get_all_properties as service_get_all_property,
get_property_by_id as service_get_property_by_id, create_property as service_create_property)
from utils.helper_functions import serialize_sqlalchemy_objects
from models.base import SessionLocal

db = SessionLocal()

# récupérer toutes les propriétés
#properties = get_all_property(db)
#print("Toutes les propriétés:")
#for p in properties:
 #   print(p.PropertyID, p.Address)

properties = service_get_all_property(db)
print('all properties :')
all_data = serialize_sqlalchemy_objects(properties)
print(all_data)

prop = service_get_property_by_id(db,2)

print(prop)

# récupérer toutes les locataires
tenants = get_all_tenants(db)
print("Tous les locataires:")
for t in tenants:
    print(t.TenantID, t.Name)


t = get_tenant_by_id(db,2)

if t:
    print("ID:", t.TenantID)
    print("Name:", t.Name)
    print("Contact Info :", t.ContactInfo)
    print("LeaseTermStart:", t.LeaseTermStart)
    print("Date achat:", t.LeaseTermEnd)

else:
    print("Aucun locataire trouvée")


# récupérer toutes les maintenances
maintenances = get_all_maintenances(db)
print("Toutes les maintenance:")
for m in maintenances:
    print(m.TaskID, m.Description)


m = get_maintenance_by_id(db,2)

if m:
    print("ID:", m.TaskID)
    print("Description :", m.Description)
    print("Status :", m.Status)
    print("Scheduled Date:", m.ScheduledDate)
else:
    print("Aucun maintenance trouvée")

data = {
    "Address": "3 Quai de Grenelle, Marseille, 13002",
    "PropertyType": "residential",
    "Status": "Occupied",
    "PurchaseDate":"2020-06-15",
    "Price":"2000"
}
print("Create property")
create_property = service_create_property(db,data)
print(create_property)