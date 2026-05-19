def calculate_threat_score(alert):

    score = 0

    alert_type = alert.get(
        "alert_type",
        ""
    )

    if alert_type == "Open Network":
        score += 80

    elif alert_type == "Weak Encryption":
        score += 60

    elif alert_type == "Duplicate SSID":
        score += 40

    else:
        score += 20

    return score

def classify_severity(score):

    if score >= 80:
        return "critical"

    elif score >= 60:
        return "high"

    elif score >= 40:
        return "medium"

    else:
        return "low"
    
def enrich_alerts(alerts):

    enriched_alerts = []

    for alert in alerts:

        score = calculate_threat_score(
            alert
        )

        severity = classify_severity(
            score
        )

        alert["threat_score"] = score

        alert["severity"] = severity

        enriched_alerts.append(alert)

    return enriched_alerts