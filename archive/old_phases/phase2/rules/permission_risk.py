HIGH_RISK_PERMISSIONS = {
    "android.permission.READ_SMS": "Permission frequently abused by malware",
    "android.permission.RECEIVE_SMS": "Can intercept incoming SMS",
    "android.permission.RECEIVE_BOOT_COMPLETED": "Allows persistence after reboot",
    "android.permission.BIND_ACCESSIBILITY_SERVICE": "Grants powerful control over device",
}

# Permission combination abuse patterns
PERMISSION_COMBOS = [
    (
        {"android.permission.READ_SMS", "android.permission.RECEIVE_SMS"},
        "OTP theft via SMS interception"
    ),
    (
        {"android.permission.READ_SMS", "android.permission.INTERNET"},
        "SMS data exfiltration to remote server"
    ),
    (
        {"android.permission.RECEIVE_BOOT_COMPLETED", "android.permission.INTERNET"},
        "Persistent spyware with network access"
    ),
    (
        {"android.permission.BIND_ACCESSIBILITY_SERVICE", "android.permission.INTERNET"},
        "Full device takeover via accessibility abuse"
    ),
]

def analyze_permissions(permissions: list) -> list:
    findings = []
    perm_set = set(permissions)

    # Single permission risks
    for perm in permissions:
        if perm in HIGH_RISK_PERMISSIONS:
            findings.append({
                "type": "permission_risk",
                "permission": perm,
                "severity": "HIGH",
                "reason": HIGH_RISK_PERMISSIONS[perm]
            })

    # Combination abuse detection
    for combo, reason in PERMISSION_COMBOS:
        if combo.issubset(perm_set):
            findings.append({
                "type": "permission_combo_abuse",
                "permissions": list(combo),
                "severity": "CRITICAL",
                "reason": reason
            })

    return findings
