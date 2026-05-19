import re


def parse_wifi_output(raw_text):
    networks = []

    current_network = {}

    lines = raw_text.splitlines()

    for line in lines:
        line = line.strip()

        # SSID
        if line.startswith("SSID"):
            if current_network:
                networks.append(current_network)

            ssid = line.split(":", 1)[1].strip()

            current_network = {
                "ssid": ssid
            }

        # Authentication
        elif line.startswith("Authentication"):
            current_network["authentication"] = (
                line.split(":", 1)[1].strip()
            )

        # Encryption
        elif line.startswith("Encryption"):
            current_network["encryption"] = (
                line.split(":", 1)[1].strip()
            )

        # BSSID
        elif line.startswith("BSSID"):
            current_network["bssid"] = (
                line.split(":", 1)[1].strip()
            )

        # Signal
        elif line.startswith("Signal"):
            signal = line.split(":", 1)[1].strip()
            signal = signal.replace("%", "")

            current_network["signal"] = int(signal)

        # Band
        elif line.startswith("Band"):
            current_network["band"] = (
                line.split(":", 1)[1].strip()
            )

        # Channel
        elif line.startswith("Channel"):
            channel = line.split(":", 1)[1].strip()

            if channel.isdigit():
                current_network["channel"] = int(channel)

    # Add final network
    if current_network:
        networks.append(current_network)

    return networks