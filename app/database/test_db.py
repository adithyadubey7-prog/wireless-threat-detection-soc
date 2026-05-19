from app.database.db import (
    initialize_database,
    insert_alert
)


sample_alert = {

    "alert_type": "Open Network",

    "severity": "critical",

    "ssid": "CoffeeShopWiFi",

    "message": "Open wireless network detected",

    "threat_score": 80
}


initialize_database()

insert_alert(sample_alert)

print("Alert inserted successfully.")