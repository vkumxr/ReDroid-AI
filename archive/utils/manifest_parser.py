"""
utils/manifest_parser.py
Parses AndroidManifest.xml (decoded by apktool) to extract permissions, components, etc.
"""
import xml.etree.ElementTree as ET
from typing import Dict, List
import re
from pathlib import Path

ANDROID_NS = "http://schemas.android.com/apk/res/android"

def _ns(tag: str) -> str:
    return f"{{{ANDROID_NS}}}{tag}"

def parse_manifest(manifest_path: str) -> Dict:
    """
    Parse an AndroidManifest.xml file extracted by apktool.
    Returns a dictionary with package, permissions, activities, services, receivers, providers.
    """
    res = {
        "package": None,
        "permissions": [],
        "activities": [],
        "services": [],
        "receivers": [],
        "providers": [],
        "intent_filters": []
    }

    if not Path(manifest_path).exists():
        raise FileNotFoundError(f"{manifest_path} not found")

    tree = ET.parse(manifest_path)
    root = tree.getroot()
    res["package"] = root.attrib.get("package")

    # Permissions
    for perm in root.findall("uses-permission"):
        name = perm.attrib.get(_ns("name")) or perm.attrib.get("android:name")
        if name:
            res["permissions"].append(name)

    # Components: activities, services, receivers, providers
    app = root.find("application")
    if app is not None:
        for tag, store in [
            ("activity", res["activities"]),
            ("service", res["services"]),
            ("receiver", res["receivers"]),
            ("provider", res["providers"])
        ]:
            for node in app.findall(tag):
                nm = node.attrib.get(_ns("name")) or node.attrib.get("android:name")
                if nm:
                    store.append(nm)

                # collect declared intent-filters (simple representation)
                for ifilter in node.findall("intent-filter"):
                    actions = [a.attrib.get(_ns("name")) or a.attrib.get("android:name") for a in ifilter.findall("action")]
                    categories = [c.attrib.get(_ns("name")) or c.attrib.get("android:name") for c in ifilter.findall("category")]
                    if actions or categories:
                        res["intent_filters"].append({
                            "component": nm,
                            "actions": [x for x in actions if x],
                            "categories": [x for x in categories if x]
                        })

    # Normalize unique lists
    for k in ["permissions", "activities", "services", "receivers", "providers"]:
        res[k] = list(dict.fromkeys(res[k]))  # preserve order, unique

    return res