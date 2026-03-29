def analyze_ticket(description: str):
    desc = description.lower()

    if "password" in desc or "login" in desc:
        return {
            "category": "Access",
            "severity": "High",
            "department": "IT",
            "resolution": "Auto-resolve"
        }

    elif "database" in desc or "db" in desc:
        return {
            "category": "DB",
            "severity": "Critical",
            "department": "Engineering",
            "resolution": "Assign"
        }

    elif "salary" in desc or "payroll" in desc:
        return {
            "category": "Finance",
            "severity": "Medium",
            "department": "Finance",
            "resolution": "Assign"
        }

    else:
        return {
            "category": "Other",
            "severity": "Low",
            "department": "Support",
            "resolution": "Assign"
        }