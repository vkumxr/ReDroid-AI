def analyze_exported_components(components: dict):
    findings = []

    for comp_type, comp_list in components.items():
        for comp in comp_list:
            if comp.get("exported") is True:
                findings.append({
                    "type": "exported_component",
                    "component_type": comp_type,
                    "name": comp.get("name"),
                    "severity": "HIGH" if comp_type in ["receiver", "service"] else "MEDIUM",
                    "reason": "Exported component can be invoked by other apps"
                })

    return findings
