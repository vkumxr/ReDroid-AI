SUSPICIOUS_COMBOS = [
    {
        "combo": {
            "android.permission.READ_SMS",
            "android.permission.RECEIVE_BOOT_COMPLETED"
        },
        "severity": "CRITICAL",
        "reason": "SMS interception with persistence across reboots"
    },
    {
        "combo": {
            "android.permission.SYSTEM_ALERT_WINDOW",
            "android.permission.INTERNET"
        },
        "severity": "HIGH",
        "reason": "Overlay abuse commonly used in phishing"
    },
    {
        "combo": {
            "android.permission.BIND_ACCESSIBILITY_SERVICE"
        },
        "severity": "CRITICAL",
        "reason": "Accessibility services are heavily abused by malware"
    }
]


def analyze_permission_combos(permissions: list) -> list:
    findings = []
    perm_set = set(permissions)

    for rule in SUSPICIOUS_COMBOS:
        if rule["combo"].issubset(perm_set):
            findings.append({
                "type": "permission_combo",
                "permissions": list(rule["combo"]),
                "severity": rule["severity"],
                "reason": rule["reason"]
            })

    return findings