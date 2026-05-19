from wifi_scanner import scan_wifi_networks
from parser import parse_wifi_output

raw_output = scan_wifi_networks()

parsed_networks = parse_wifi_output(raw_output)

for network in parsed_networks:
    print(network)