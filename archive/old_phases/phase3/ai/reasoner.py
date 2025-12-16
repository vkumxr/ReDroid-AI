def reason(phase2_report: dict) -> dict:
    score = phase2_report.get("risk_summary", {}).get("score", 0)
    findings = phase2_report.get("findings", [])

    assessment = {
        "verdict": "BENIGN",
        "confidence": "LOW",
        "summary": [],
        "recommended_actions": []
    }

    if score >= 80:
        assessment["verdict"] = "MALICIOUS"
        assessment["confidence"] = "HIGH"
    elif score >= 40:
        assessment["verdict"] = "SUSPICIOUS"
        assessment["confidence"] = "MEDIUM"

    for f in findings:
        if f["type"] == "permission_combo_abuse":
            assessment["summary"].append(
                f"High-risk permission combination detected: {', '.join(f['permissions'])}. "
                f"Likely behavior: {f['reason']}."
            )

        if f["type"] == "exported_component":
            assessment["summary"].append(
                f"Exported {f['component_type']} ({f['name']}) may allow external triggering."
            )

    if assessment["verdict"] == "MALICIOUS":
        assessment["recommended_actions"] = [
            "Block installation",
            "Submit for dynamic analysis",
            "Inspect network traffic"
        ]
    elif assessment["verdict"] == "SUSPICIOUS":
        assessment["recommended_actions"] = [
            "Manual review recommended",
            "Run sandbox analysis"
        ]

    return assessment