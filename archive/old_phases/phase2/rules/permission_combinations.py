DANGEROUS_COMBINATIONS = [
    {
        "permissions": {
            "android.permission.READ_SMS",
            "android.permission.RECEIVE_BOOT_COMPLETED"
        },
        "severity": "CRITICAL",
        "reason": "SMS interception with boot persistence"
    },
    {
        "permissions": {
            "android.permission.SYSTEM_ALERT_WINDOW",
            "android.permission.INTERNET"
        },
        "severity": "HIGH",
        "reason": "Overlay-based phishing capability"
    },
    {
        "permissions": {
            "android.permission.BIND_ACCESSIBILITY_SERVICE",
            "android.permission.INTERNET"
        },
        "severity": "CRITICAL",
        "reason": "Accessibility abuse enabling full device control"
    }
]

def analyze_permission_combinations(permissions: list) -> list:
    findings = []
    perm_set = set(permissions)

    for combo in DANGEROUS_COMBINATIONS:
        if combo["permissions"].issubset(perm_set):
            findings.append({
                "type": "permission_combination",
                "permissions": list(combo["permissions"]),
                "severity": combo["severity"],
                "reason": combo["reason"]
            })

    return findings
