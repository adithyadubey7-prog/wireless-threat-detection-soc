import sqlite3
import json
from datetime import datetime, timedelta

def convert_to_ist(timestamp_string):

    utc_time = datetime.strptime(

        timestamp_string,

        "%Y-%m-%d %H:%M:%S"
    )

    ist_time = utc_time + timedelta(

        hours=5,

        minutes=30
    )

    return ist_time.strftime(

        "%d-%m-%Y %I:%M:%S %p"
    )

DATABASE_NAME = "wireless_soc.db"


def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    return connection

def alert_exists(alert):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        SELECT id

        FROM alerts

        WHERE

            alert_type = ?
            AND ssid = ?
            AND severity = ?

    """, (

        alert["alert_type"],

        alert["ssid"],

        alert["severity"]

    ))

    result = cursor.fetchone()

    connection.close()

    return result is not None

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()


    # Remove old broken tables
    cursor.execute("""
        DROP TABLE IF EXISTS alerts
    """)

    cursor.execute("""
        DROP TABLE IF EXISTS scan_history
    """)


    # Create alerts table
    cursor.execute("""

        CREATE TABLE alerts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME
            DEFAULT CURRENT_TIMESTAMP,

            alert_type TEXT,

            severity TEXT,

            ssid TEXT,

            message TEXT,

            threat_score INTEGER,
                   
            details TEXT,

            status TEXT DEFAULT 'new'     
        )

    """)


    # Create scan history table
    cursor.execute("""

        CREATE TABLE scan_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME
            DEFAULT CURRENT_TIMESTAMP,

            networks_detected INTEGER,

            alerts_generated INTEGER
        )

    """)

    connection.commit()

    connection.close()

def insert_alert(alert):

    if alert_exists(alert):
        return

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        INSERT INTO alerts (

            alert_type,
            severity,
            ssid,
            message,
            threat_score,
            details,
            status

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        alert["alert_type"],
        alert["severity"],
        alert["ssid"],
        alert["message"],
        alert["threat_score"],

        json.dumps(

        alert.get(
            "related_networks",
            []
        )
        ),

        "new"

    ))

    connection.commit()

    connection.close()

def insert_scan_history(
    networks_detected,
    alerts_generated
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        INSERT INTO scan_history (

            networks_detected,
            alerts_generated

        )

        VALUES (?, ?)

    """, (

        networks_detected,
        alerts_generated

    ))

    connection.commit()

    connection.close()

def get_all_alerts():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        SELECT
            id,
            timestamp,
            alert_type,
            severity,
            ssid,
            message,
            threat_score,
            details,
            status

        FROM alerts

        ORDER BY
            threat_score DESC,
            timestamp DESC

    """)

    rows = cursor.fetchall()

    alerts = []

    for row in rows:

        alerts.append({

            "id": row[0],

            "timestamp": convert_to_ist(row[1]),

            "alert_type": row[2],

            "severity": row[3],

            "ssid": row[4],

            "message": row[5],

            "threat_score": row[6],

            "details": json.loads(row[7]),
            "status": row[8]
        })

    connection.close()

    return alerts

def get_scan_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        SELECT
            timestamp,
            networks_detected,
            alerts_generated

        FROM scan_history

        ORDER BY id ASC

    """)

    rows = cursor.fetchall()

    connection.close()


    history = []

    for row in rows:

        history.append({

            "timestamp": convert_to_ist(row[0]),

            "networks_detected": row[1],

            "alerts_generated": row[2]
        })

    return history

def update_alert_status(
    alert_id,
    status
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        UPDATE alerts

        SET status = ?

        WHERE id = ?

    """, (

        status,
        alert_id
    ))

    connection.commit()

    connection.close()