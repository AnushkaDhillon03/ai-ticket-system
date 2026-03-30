from fastapi import FastAPI
from pydantic import BaseModel
from database import engine, SessionLocal
from models import Base, Ticket, Employee
from ai_engine import analyze_ticket

app = FastAPI()

Base.metadata.create_all(bind=engine)

# -------------------------------
# Seed Employees
# -------------------------------
def seed_employees():
    db = SessionLocal()

    if db.query(Employee).count() == 0:
        employees = [
            Employee(name="Rahul", email="rahul@company.com", role="IT Support", department="IT", skill="Access", current_load=2, availability="Available"),
            Employee(name="Ankit", email="ankit@company.com", role="Backend Engineer", department="Engineering", skill="DB", current_load=1, availability="Available"),
            Employee(name="Neha", email="neha@company.com", role="Finance Executive", department="Finance", skill="Payroll", current_load=3, availability="Busy"),
            Employee(name="Riya", email="riya@company.com", role="Network Engineer", department="Support", skill="Network", current_load=1, availability="Available"),
        ]

        db.add_all(employees)
        db.commit()

    db.close()

seed_employees()

# -------------------------------
# Smart Assignment
# -------------------------------
def assign_employee(department):
    db = SessionLocal()

    employees = db.query(Employee).filter(
        Employee.department == department,
        Employee.availability == "Available"
    ).order_by(Employee.current_load).all()

    if employees:
        selected = employees[0]

        name = selected.name
        email = selected.email
        role = selected.role

        selected.current_load += 1
        db.commit()
        db.close()

        return f"{name} ({role}) - {email}"

    db.close()
    return "Support Team (fallback)"

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

        status = "Resolved" if ai_result["resolution"] == "Auto-resolve" else "Assigned"

        new_ticket = Ticket(
            description=ticket.description,
            category=ai_result["category"],
            severity=ai_result["severity"],
            status=status,
            department=ai_result["department"],
            assigned_to=employee,
            timeline=f"Created -> {status}"
        )

        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)

        # Auto-response
        if ai_result["resolution"] == "Auto-resolve":
            response_message = f"""
We have analyzed your issue:

{ai_result['summary']}

Suggested resolution:
Please follow the standard steps.

Estimated time: {ai_result['estimated_time']}

Was this helpful? (Yes / No)
"""
        else:
            response_message = f"""
Assigned to {employee}

Department: {ai_result['department']}
Severity: {ai_result['severity']}
Estimated time: {ai_result['estimated_time']}
"""

        return {
            "ticket_id": new_ticket.id,
            "description": ticket.description,
            "ai_analysis": ai_result,
            "assigned_to": employee,
            "status": status,
            "response": response_message
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()


@app.put("/ticket/{ticket_id}/status")
def update_status(ticket_id: int, new_status: str, note: str = ""):
    db = SessionLocal()

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        return {"error": "Ticket not found"}

    ticket.status = new_status

    if note:
        ticket.notes += f"\n{note}"

    ticket.timeline += f" -> {new_status}"

    db.commit()
    db.refresh(ticket)

    db.close()

    return {
        "ticket_id": ticket.id,
        "status": ticket.status,
        "notes": ticket.notes,
        "timeline": ticket.timeline
    }

# -------------------------------
# GET TICKET DETAILS
# -------------------------------
@app.get("/ticket/{ticket_id}")
def get_ticket(ticket_id: int):
    db = SessionLocal()

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        return {"error": "Ticket not found"}

    db.close()

    return {
        "ticket_id": ticket.id,
        "description": ticket.description,
        "status": ticket.status,
        "assigned_to": ticket.assigned_to,
        "timeline": ticket.timeline,
        "notes": ticket.notes
    }

# -------------------------------
# ANALYTICS
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
