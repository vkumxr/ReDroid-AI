HIGH_RISK_PERMISSIONS = {
    "android.permission.READ_SMS",
    "android.permission.RECEIVE_SMS",
    "android.permission.SEND_SMS",
    "android.permission.BIND_ACCESSIBILITY_SERVICE",
    "android.permission.SYSTEM_ALERT_WINDOW",
    "android.permission.READ_CALL_LOG"
}

def analyze_permissions(permissions: list) -> list:
    findings = []

    for perm in permissions:
        if perm in HIGH_RISK_PERMISSIONS:
            findings.append({
                "type": "permission_risk",
                "permission": perm,
                "severity": "HIGH",
                "reason": "Permission frequently abused by malware"
            })

    return findings
