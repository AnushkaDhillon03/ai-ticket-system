from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    category = Column(String)
    severity = Column(String)
    status = Column(String)
    department = Column(String)
    assigned_to = Column(String)

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    department = Column(String)
    skill = Column(String)
    current_load = Column(Integer)
    availability = Column(String)