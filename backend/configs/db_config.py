import os
from dotenv import load_dotenv
#from sqlalchemy import create_engine   # <-- manquait
#from sqlalchemy.orm import sessionmaker
#from models.base import Base
#from models.property import Property
#from models.tenant import Tenant
#from models.maintenance import Maintenance
#from utils.helper_functions import import_csv_file
class Config:
    load_dotenv()   

    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_PORT = os.getenv('DATABASE_PORT')
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    DATABASE_NAME = os.getenv('DATABASE_NAME')

    DATABASE_URL = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#csv_file = ["./fichier_csv/properties.csv", "./fichier_csv/tenants.csv","./fichier_csv/maintenance.csv"]



#try:
 #   Base.metadata.drop_all(bind=engine)
  #  Base.metadata.create_all(bind=engine)
   # import_csv_file(csv_file,engine)
    #print("success")

#except Exception as ex:
   #print(ex)
