from collections import Counter

from collections import defaultdict


def detect_duplicate_ssids(networks):

    alerts = []

    ssid_groups = defaultdict(list)


    # Group networks by SSID
    for network in networks:

        ssid = network["ssid"].strip()

        if ssid != "":

            ssid_groups[ssid].append(
                network
            )


    # Analyze duplicates
    for ssid, group in ssid_groups.items():

        if len(group) > 1:

            channels = set([
                net["channel"]
                for net in group
            ])

            auth_types = set([
                net["authentication"]
                for net in group
            ])

            signals = [
                net["signal"]
                for net in group
            ]

            signal_difference = (
                max(signals) - min(signals)
            )


            suspicion_score = 0


            # Different channels
            if len(channels) > 1:
                suspicion_score += 1


            # Different authentication
            if len(auth_types) > 1:
                suspicion_score += 2


            # Large signal variance
            if signal_difference > 40:
                suspicion_score += 1


            # Only alert if suspicious enough
            if suspicion_score >= 2:

                alerts.append({

                    "alert_type":
                        "Possible Evil Twin",

                    "severity":
                        "high",

                    "ssid": ssid,

                    "message":
                        f"SSID '{ssid}' shows suspicious "
                        f"multi-AP behavior",

                    "related_networks": group
                })
            return alerts

def detect_open_networks(networks):
    """
    Detect open wireless networks.
    """

    alerts = []

    for network in networks:

        authentication = network.get(
            "authentication",
            ""
        ).lower()

        if "open" in authentication:

            alerts.append({
                "alert_type": "Open Network",
                "severity": "high",
                "ssid": (
                    network["ssid"]
                    if network["ssid"].strip() != ""
                    else "[HIDDEN SSID]"
                ),
                "message": (
                    "Open wireless network detected"
                )
            })

    return alerts


def detect_weak_encryption(networks):
    """
    Detect weak wireless encryption.
    """

    alerts = []

    weak_protocols = [
        "wep",
        "wpa"
    ]

    for network in networks:

        authentication = network.get(
            "authentication",
            ""
        ).lower()

        for weak in weak_protocols:

            if (
                weak in authentication
                and "wpa2" not in authentication
                and "wpa3" not in authentication
            ):

                alerts.append({
                    "alert_type": "Weak Encryption",
                    "severity": "medium",
                    "ssid": network["ssid"],
                    "message": (
                        f"Weak wireless security "
                        f"detected: {authentication}"
                    )
                })

    return alerts


def run_all_detections(networks):
    """
    Run all wireless detection rules.
    """

    alerts = []

    alerts.extend(
        detect_duplicate_ssids(networks)
    )

    alerts.extend(
        detect_open_networks(networks)
    )

    alerts.extend(
        detect_weak_encryption(networks)
    )

    return alerts