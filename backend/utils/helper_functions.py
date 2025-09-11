import re
import csv
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
import json


def validate_property_data(data:dict):
    if data.get("PropertyType") not in ("Residential", "Commercial"):
        raise ValueError("PropertyType must be 'Residential' or 'Commercial'")
    if data.get("Status") not in ("Occupied", "Vacant"):
        raise ValueError("Status must be 'Occupied' or 'Vacant'")
    return True

FRENCH_PHONE_RE = re.compile(r'^(?:\+33|0)[1-9](?:\d{2}){4}$')

def validate_tenant_data(data: dict):
    phone = data.get("ContactInfo")
    if not FRENCH_PHONE_RE.fullmatch(phone):
        raise ValueError("ContactInfo must be a valid French phone number (+33... or 0...).")
    if data.get("RentalPaymentStatus") not in ("Pending", "Paid"):
        raise ValueError("RentalPaymentStatus must be one of: pending, paid")
    return True

def validate_maintenance_data(data: dict):
    if data.get("Status") not in ("Pending", "In Progress","Completed"):
        raise ValueError("Status must be 'Pending' or 'in Progress' or 'Completed'")
    return True

def import_properties_from_csv_with_id(file_path: str, engine):
    from models.property import Property
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        with Session(engine) as db:
            for row in reader:
                data = {
                    "PropertyID": int(row["PropertyID"]),
                    "Address": row["Address"],
                    "PropertyType": row["PropertyType"],
                    "Status": row["Status"],
                    "PurchaseDate": datetime.strptime(row["PurchaseDate"], "%Y-%m-%d").date(),
                    "Price": int(row["Price"])
                }

                # Vérifier si PropertyID existe déjà
                existing = db.query(Property).filter_by(PropertyID=data["PropertyID"]).first()
                if existing:
                    print(f"PropertyID déjà existant : {data['PropertyID']}, skip")
                    continue

                prop = Property(**data)
                db.add(prop)
            db.commit()

    # Mettre à jour la séquence pour éviter les conflits futurs
    with engine.connect() as conn:
        conn.execute(text(f"""
            SELECT setval(
                pg_get_serial_sequence('property', 'PropertyID'),
                (SELECT COALESCE(MAX("PropertyID"), 1) FROM property)
            )
        """))
        conn.commit()

    print("Import terminé ! Séquence mise à jour.")

def import_tenants_from_csv_with_id(file_path: str, engine):
    from models.tenant import Tenant
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        with Session(engine) as db:
            for row in reader:
                data = {
                    "TenantID": int(row["TenantID"]),
                    "Name": row["Name"],
                    "ContactInfo": row["ContactInfo"],
                    "LeaseTermStart": datetime.strptime(row["LeaseTermStart"], "%Y-%m-%d").date(),
                    "LeaseTermEnd": datetime.strptime(row["LeaseTermEnd"], "%Y-%m-%d").date(),
                    "RentalPaymentStatus": row["RentalPaymentStatus"],
                    "PropertyID": row["PropertyID"],
                }
                # Vérifier si TenantID existe déjà
                existing = db.query(Tenant).filter_by(TenantID=data["TenantID"]).first()
                if existing:
                    print(f"TenantID déjà existant : {data['TenantID']}, skip")
                    continue

                tenant = Tenant(**data)
                db.add(tenant)
            db.commit()

    # Mettre à jour la séquence pour éviter les conflits futurs
    with engine.connect() as conn:
        conn.execute(text(f"""
            SELECT setval(
                pg_get_serial_sequence('tenant', 'TenantID'),
                (SELECT COALESCE(MAX("TenantID"), 1) FROM tenant)
            )
        """))
        conn.commit()

    print("Import terminé ! Séquence mise à jour.")

def import_maintenances_from_csv_with_id(file_path: str,engine):
    from models.maintenance import Maintenance
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        with Session(engine) as db:
            for row in reader:
                data = {
                    "TaskID": int(row["TaskID"]),
                    "Description": row["Description"],
                    "Status": row["Status"],
                    "ScheduledDate": datetime.strptime(row["ScheduledDate"], "%Y-%m-%d").date(),
                    "PropertyID": row["PropertyID"],
                }

                # Vérifier si TaskID existe déjà
                existing = db.query(Maintenance).filter_by(TaskID=data["TaskID"]).first()
                if existing:
                    print(f"TaskID déjà existant : {data['TaskID']}, skip")
                    continue

                maintenance = Maintenance(**data)
                db.add(maintenance)
            db.commit()

    # Mettre à jour la séquence pour éviter les conflits futurs
    with engine.connect() as conn:
        conn.execute(text(f"""
            SELECT setval(
                pg_get_serial_sequence('maintenance', 'TaskID'),
                (SELECT COALESCE(MAX("TaskID"), 1) FROM maintenance)
            )
        """))
        conn.commit()

    print("Import terminé ! Séquence mise à jour.")


def import_csv_file(csv_file,engine) -> None:

    import_properties_from_csv_with_id(csv_file[0], engine)
    import_tenants_from_csv_with_id(csv_file[1], engine)
    import_maintenances_from_csv_with_id(csv_file[2],engine)


def serialize_sqlalchemy_objects(objects):
    """
    Transforme une liste d'objets SQLAlchemy en dictionnaires prêts pour JSON.
    
    Args:
        objects (list): Liste d'objets SQLAlchemy ou de dictionnaires (__dict__).
    
    Returns:
        list: Liste de dictionnaires nettoyés, dates converties en string.
    """
    import datetime
    serialized = []

    for obj in objects:
        # Si c'est un objet SQLAlchemy, récupérer son __dict__, sinon on suppose que c'est déjà un dict
        obj_dict = obj.__dict__ if not isinstance(obj, dict) else obj

        # Supprimer l'état interne SQLAlchemy
        clean_dict = {k: v for k, v in obj_dict.items() if k != '_sa_instance_state'}

        # Convertir les dates en string ISO
        for k, v in clean_dict.items():
            if isinstance(v, datetime.date):
                clean_dict[k] = v.isoformat()
        
        serialized.append(clean_dict)
    
    return serialized

def serialize_object(obj):
    import datetime
    """
    Transforme un objet SQLAlchemy en dictionnaire prêt pour JSON.
    
    Args:
        obj: Objet SQLAlchemy.
    
    Returns:
        dict: Dictionnaire nettoyé, dates converties en string.
    """
    if obj != None:
        obj_dict = obj.__dict__.copy()  # copier pour ne pas modifier l'objet original
        # Supprimer l'état interne SQLAlchemy
        obj_dict.pop('_sa_instance_state', None)
        
        # Convertir les dates en string ISO
        for k, v in obj_dict.items():
            if isinstance(v, datetime.date):
                obj_dict[k] = v.isoformat()
        
        return obj_dict

