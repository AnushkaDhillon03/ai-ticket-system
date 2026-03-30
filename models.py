from sqlalchemy import Column, Integer, String, Text
from database import Base

# -------------------------------
# Ticket Model (WITH LIFECYCLE)
# -------------------------------
class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    category = Column(String)
    severity = Column(String)

    # lifecycle
    status = Column(String)
    department = Column(String)
    assigned_to = Column(String)

    notes = Column(Text, default="")
    timeline = Column(Text, default="Created")


# -------------------------------
# Employee Model (UPGRADED)
# -------------------------------
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    email = Column(String)      # ✅ added
    role = Column(String)       # ✅ added

    department = Column(String)
    skill = Column(String)
    current_load = Column(Integer)
    availability = Column(String)
