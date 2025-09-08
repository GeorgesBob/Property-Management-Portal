from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from .base import Base
from .tenant import Tenant
from .maintenance import Maintenance


class Property(Base):
    __tablename__ = "property"   # <-- double underscore

    PropertyID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Address = Column(String, nullable=False)
    PropertyType = Column(String, nullable=False)
    Status = Column(String, nullable=False)
    PurchaseDate = Column(Date, nullable=False)
    Price = Column(Integer, nullable=False)
    tenants = relationship("Tenant", back_populates="property")
    maintenances = relationship("Maintenance", back_populates="property")