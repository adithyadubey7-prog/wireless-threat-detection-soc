import subprocess


def scan_wifi_networks():
    command = ["netsh", "wlan", "show", "networks", "mode=bssid"]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    return result.stdout


if __name__ == "__main__":
    output = scan_wifi_networks()
    print(output)