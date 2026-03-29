AI Ticketing System

An AI-powered ticket management system that automatically classifies, prioritizes, and assigns support tickets based on their description.

---

## 🚀 Features

* 🔍 AI-based ticket analysis (category, severity, department)
* ⚡ Auto-resolution for simple issues (e.g., password reset)
* 🧠 Smart employee assignment based on workload
* 🏢 Department-based routing (IT, Engineering, Support, etc.)
* 📊 Analytics dashboard (API-based)
* 💾 Database integration using SQLite
* ⚙️ FastAPI backend with interactive Swagger UI

---

## 🛠️ Tech Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic

---

## 📂 Project Structure

```
ai-ticket-system/
│
├── main.py           # Main FastAPI app
├── models.py         # Database models
├── database.py       # DB connection setup
├── ai_engine.py      # AI logic (rule-based)
├── requirements.txt  # Dependencies
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd ai-ticket-system
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

### 5. Open in browser

```
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints

### 🏠 Home

```
GET /
```

### 🎫 Create Ticket

```
POST /ticket
```

Example:

```json
{
  "description": "Network is slow"
}
```

---

### 📊 Analytics

```
GET /analytics
```

Example Response:

```json
{
  "total_tickets": 2,
  "resolved": 1,
  "assigned": 1
}
```

---

## 🧠 How It Works

1. User submits a ticket description
2. AI engine analyzes the text
3. System determines:

   * category
   * severity
   * department
4. Ticket is either:

   * auto-resolved OR
   * assigned to the best employee
5. Data is stored in the database
6. Analytics API tracks system performance

---

## 📊 Example Outputs

| Description      | Category | Severity | Department  | Resolution   |
| ---------------- | -------- | -------- | ----------- | ------------ |
| Forgot password  | Access   | High     | IT          | Auto-resolve |
| Database is down | DB       | Critical | Engineering | Assign       |
| Network issue    | Network  | Low      | Support     | Assign       |

---

## ⚠️ Limitations

* AI logic is rule-based (not using real LLM)
* No frontend UI (API-based system)
* Limited analytics

---

## 🚀 Future Improvements

* Integrate real AI model (OpenAI / LLM)
* Build frontend dashboard (React)
* Add email notifications
* Advanced analytics & charts

---

## 🎯 Conclusion

This project demonstrates how AI can automate ticket classification, routing, and resolution, reducing manual effort and improving efficiency in support systems.

---

## 👩‍💻 Author

Anushka Dhillon
