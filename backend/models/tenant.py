from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base import Base 

class Tenant(Base):
    __tablename__ = "tenant"
    TenantID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String, nullable = False)
    ContactInfo = Column(String, nullable=False)
    LeaseTermStart = Column(Date, nullable=False)
    LeaseTermEnd = Column(Date, nullable=False)
    RentalPaymentStatus = Column(String, nullable=False)
    PropertyID = Column(Integer, ForeignKey("property.PropertyID"))
    property = relationship("Property", back_populates="tenants")
