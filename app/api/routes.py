from fastapi import APIRouter

from app.database.db import (
    get_all_alerts
)
from app.scanner.wifi_scanner import (
    scan_wifi_networks
)

from app.database.db import (
    update_alert_status
)

from app.scanner.parser import (
    parse_wifi_output
)

from app.database.db import (
    get_scan_history
)

router = APIRouter()


@router.get("/alerts")
def fetch_alerts():

    alerts = get_all_alerts()

    return {
        "alerts": alerts
    }

@router.get("/stats")
def get_stats():

    alerts = get_all_alerts()

    history = get_scan_history()


    total_alerts = len(alerts)

    critical_alerts = len([

        alert
        for alert in alerts

        if alert["severity"] == "critical"
    ])


    duplicate_ssids = len([

        alert
        for alert in alerts

        if "Duplicate" in alert["alert_type"]
    ])


    total_networks = 0

    if history:

        total_networks = history[-1][
            "networks_detected"
        ]


    last_scan = "N/A"

    if history:

        last_scan = history[-1][
            "timestamp"
        ]


    return {

        "total_networks":
            total_networks,

        "total_alerts":
            total_alerts,

        "critical_alerts":
            critical_alerts,

        "duplicate_ssids":
            duplicate_ssids,

        "last_scan":
            last_scan
    }

@router.get("/severity-data")
def severity_data():

    alerts = get_all_alerts()


    critical = len([

        alert
        for alert in alerts

        if alert["severity"] == "critical"
    ])

    high = len([

        alert
        for alert in alerts

        if alert["severity"] == "high"
    ])

    medium = len([

        alert
        for alert in alerts

        if alert["severity"] == "medium"
    ])

    low = len([

        alert
        for alert in alerts

        if alert["severity"] == "low"
    ])


    return {

        "labels": [

            "Critical",

            "High",

            "Medium",

            "Low"
        ],

        "values": [

            critical,

            high,

            medium,

            low
        ]
    }

@router.get("/trend-data")
def trend_data():

    try:

        history = get_scan_history()

        return {
            "history": history
        }

    except Exception as error:

        return {
            "error": str(error)
        }
    
@router.post(
    "/alerts/{alert_id}/status"
)
def change_alert_status(

    alert_id: int,

    status: str
):

    update_alert_status(
        alert_id,
        status
    )

    return {
        "message":
            "Alert status updated"
    }