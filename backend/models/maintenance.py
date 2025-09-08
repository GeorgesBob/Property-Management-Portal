from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Maintenance(Base):
    __tablename__ = "maintenance"

    TaskID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Description = Column(String, nullable=False)
    Status = Column(String, nullable=False)
    ScheduledDate = Column(Date)
    PropertyID = Column(Integer, ForeignKey("property.PropertyID"))
    property = relationship("Property", back_populates="maintenances")
 
    