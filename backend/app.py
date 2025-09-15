from models.base import Base, engine, SessionLocal
from flask import Flask
from controllers.property_controller import property_bp
from controllers.maintenance_controller import maintenance_bp
from controllers.tenant_controller import tenant_bp
from utils.helper_functions import import_csv_file
from flask_cors import CORS
from models.property import Property

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

csv_file = ["./fichier_csv/properties.csv", "./fichier_csv/tenants.csv", "./fichier_csv/maintenance.csv"]

app.register_blueprint(property_bp, url_prefix="/property")
app.register_blueprint(maintenance_bp, url_prefix="/maintenance")
app.register_blueprint(tenant_bp, url_prefix="/tenant")

try:
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    data_exists = session.query(Property).first()
    session.close()

    if not data_exists:
        import_csv_file(csv_file, engine)
        print("Import effectué (premier lancement)")
    else:
        print(" Données déjà présentes, import ignoré")

except Exception as ex:
    print("Une erreur est survenue :", ex)

if __name__ == "__main__":
   app.run(port=8000, debug=True)
