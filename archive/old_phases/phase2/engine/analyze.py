from phase2.rules.permission_risk import analyze_permissions

def analyze(phase1_report: dict) -> dict:
    permissions = phase1_report.get("permissions", [])
    findings = analyze_permissions(permissions)

    risk_score = 0
    for f in findings:
        if f["severity"] == "CRITICAL":
            risk_score += 40
        elif f["severity"] == "HIGH":
            risk_score += 20

    level = "LOW"
    if risk_score >= 60:
        level = "HIGH"
    elif risk_score > 0:
        level = "MEDIUM"

    return {
        "meta": {
            "engine": "ReDroid-AI Phase 2",
            "version": "0.3"
        },
        "risk_summary": {
            "score": risk_score,
            "level": level
        },
        "findings": findings
    }
