from app.scanner.wifi_scanner import scan_wifi_networks

from app.scanner.parser import parse_wifi_output

from app.detection.detector import run_all_detections

from app.detection.scorer import enrich_alerts

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


print("\n=== NETWORKS ===\n")

for network in parsed_networks:
    print(network)


print("\n=== ALERTS ===\n")

for alert in alerts:
    print(alert)