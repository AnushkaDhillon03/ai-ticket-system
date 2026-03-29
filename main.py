from fastapi import FastAPI
from pydantic import BaseModel
from database import engine, SessionLocal
from models import Base, Ticket, Employee
from ai_engine import analyze_ticket

app = FastAPI()

Base.metadata.create_all(bind=engine)

# -------------------------------
# Seed Employees (FINAL)
# -------------------------------
def seed_employees():
    db = SessionLocal()

    if db.query(Employee).count() == 0:
        employees = [
            Employee(name="Rahul", department="IT", skill="Access", current_load=2, availability="Available"),
            Employee(name="Ankit", department="Engineering", skill="DB", current_load=1, availability="Available"),
            Employee(name="Neha", department="Finance", skill="Payroll", current_load=3, availability="Busy"),
            Employee(name="Riya", department="Support", skill="Network", current_load=1, availability="Available"),  # ✅ FIXED
        ]

        db.add_all(employees)
        db.commit()

    db.close()

seed_employees()

# -------------------------------
# Smart Assignment (FINAL FIX)
# -------------------------------
def assign_employee(department):
    db = SessionLocal()

    employees = db.query(Employee).filter(
        Employee.department == department,
        Employee.availability == "Available"
    ).order_by(Employee.current_load).all()

    if employees:
        selected = employees[0]

        # ✅ FIX (save before closing session)
        employee_name = selected.name

        selected.current_load += 1
        db.commit()
        db.close()

        return employee_name

    db.close()
    return "Support Team (fallback)"  # ✅ fallback added

# -------------------------------
# Request Model
# -------------------------------
class TicketInput(BaseModel):
    description: str

# -------------------------------
# Home
# -------------------------------
@app.get("/")
def home():
    return {"message": "AI Ticket System Running 🚀"}

# -------------------------------
# Create Ticket
# -------------------------------
@app.post("/ticket")
def create_ticket(ticket: TicketInput):
    db = SessionLocal()

    try:
        ai_result = analyze_ticket(ticket.description)

        employee = assign_employee(ai_result["department"])

        new_ticket = Ticket(
            description=ticket.description,
            category=ai_result["category"],
            severity=ai_result["severity"],
            status="Resolved" if ai_result["resolution"] == "Auto-resolve" else "Assigned",
            department=ai_result["department"],
            assigned_to=employee
        )

        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)

        if ai_result["resolution"] == "Auto-resolve":
            response_message = "Your issue has been resolved automatically."
        else:
            response_message = f"Your issue has been assigned to {employee} from {ai_result['department']} department."

        return {
            "ticket_id": new_ticket.id,
            "description": ticket.description,
            "ai_analysis": ai_result,
            "assigned_to": employee,
            "status": new_ticket.status,
            "response": response_message
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()

# -------------------------------
# Analytics
# -------------------------------
@app.get("/analytics")
def analytics():
    db = SessionLocal()

    total = db.query(Ticket).count()
    resolved = db.query(Ticket).filter(Ticket.status == "Resolved").count()
    assigned = db.query(Ticket).filter(Ticket.status == "Assigned").count()

    db.close()

    return {
        "total_tickets": total,
        "resolved": resolved,
        "assigned": assigned
    }