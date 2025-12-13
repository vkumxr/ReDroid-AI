from phase2.rules.permission_risk import analyze_permissions

def analyze(phase1_report: dict) -> dict:
    permissions = phase1_report.get("permissions", [])
    findings = analyze_permissions(permissions)

    risk_score = len(findings) * 20

    return {
        "meta": {
            "engine": "ReDroid-AI Phase 2",
            "version": "0.1"
        },
        "risk_summary": {
            "score": risk_score,
            "level": "HIGH" if risk_score >= 40 else "MEDIUM" if risk_score > 0 else "LOW"
        },
        "findings": findings
    }