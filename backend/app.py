from models.base import Base, engine
from flask import Flask
from controllers.property_controller import property_bp
from controllers.maintenance_controller import maintenance_bp
from controllers.tenant_controller import tenant_bp
from utils.helper_functions import import_csv_file

app = Flask(__name__)

csv_file = ["./fichier_csv/properties.csv", "./fichier_csv/tenants.csv","./fichier_csv/maintenance.csv"]

try:
    #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    import_csv_file(csv_file,engine)
    print("success")
except Exception as ex:
    print(ex)

app.register_blueprint(property_bp, url_prefix="/property")
app.register_blueprint(maintenance_bp, url_prefix="/maintenance")
app.register_blueprint(tenant_bp, url_prefix="/tenant")
if __name__ == "__main__":
   app.run(debug=True)
