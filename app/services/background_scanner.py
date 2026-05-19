import threading

import time

import asyncio

from app.services.websocket_manager import (
    manager
)

from app.scanner.wifi_scanner import (
    scan_wifi_networks
)

from app.scanner.parser import (
    parse_wifi_output
)

from app.detection.detector import (
    run_all_detections
)

from app.detection.scorer import (
    enrich_alerts
)

from app.database.db import (
    insert_alert,
    insert_scan_history
)


SCAN_INTERVAL = 30


def background_scan_loop():

    while True:

        try:

            print(
                "\n[Background Scanner] "
                "Running scan..."
            )

            raw_output = scan_wifi_networks()

            parsed_networks = parse_wifi_output(
                raw_output
            )

            alerts = run_all_detections(
                parsed_networks
            )

            alerts = enrich_alerts(
                alerts
            )

            insert_scan_history(

                len(parsed_networks),

                len(alerts)
            )

            for alert in alerts:

                insert_alert(alert)

            asyncio.run(

                manager.broadcast({

                    "type": "new_alert",

                    "alert": alert
                })
            )

            print(
                f"[Background Scanner] "
                f"Networks: {len(parsed_networks)} | "
                f"Alerts: {len(alerts)}"
            )

        except Exception as error:

            print(
                f"[Background Scanner ERROR] "
                f"{error}"
            )

        time.sleep(SCAN_INTERVAL)


def start_background_scanner():

    scanner_thread = threading.Thread(

        target=background_scan_loop,

        daemon=True
    )

    scanner_thread.start()