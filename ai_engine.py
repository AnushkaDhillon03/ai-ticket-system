def analyze_ticket(description):
    desc = description.lower()

    category = "Other"
    severity = "Low"
    department = "Support"
    resolution = "Assign"
    sentiment = "Neutral"

    if "password" in desc or "login" in desc:
        category = "Access"
        severity = "High"
        department = "IT"
        resolution = "Auto-resolve"
        sentiment = "Frustrated"

    elif "database" in desc or "db" in desc:
        category = "DB"
        severity = "Critical"
        department = "Engineering"
        resolution = "Assign"
        sentiment = "Frustrated"

    elif "server" in desc:
        category = "Server"
        severity = "Critical"
        department = "Engineering"
        resolution = "Assign"
        sentiment = "Frustrated"

    elif "network" in desc or "slow" in desc:
        category = "Network"
        severity = "Medium"
        department = "Support"
        resolution = "Assign"

    elif "salary" in desc or "payroll" in desc:
        category = "Billing"
        severity = "High"
        department = "Finance"
        resolution = "Assign"

    elif "leave" in desc:
        category = "HR"
        severity = "Low"
        department = "HR"
        resolution = "Auto-resolve"
        sentiment = "Polite"

    summary = f"The user reported a {category.lower()} issue. It has been classified as {severity} priority and routed to {department}."

    confidence = "90%" if category != "Other" else "70%"

    if severity == "Critical":
        estimated_time = "1 hour"
    elif severity == "High":
        estimated_time = "30 minutes"
    elif severity == "Medium":
        estimated_time = "15 minutes"
    else:
        estimated_time = "5-10 minutes"

    return {
        "category": category,
        "severity": severity,
        "department": department,
        "resolution": resolution,
        "summary": summary,
        "sentiment": sentiment,
        "confidence": confidence,
        "estimated_time": estimated_time
    }
