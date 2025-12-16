"""
utils/string_scanner.py
Lightweight scanners to detect endpoints, IPs, keys, suspicious commands, & heuristics.
"""
import re
from typing import Dict, List

URL_RE = re.compile(r"""(?:(?:http|https)://[^\s'"]+)""", re.IGNORECASE)
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
BASE64_RE = re.compile(r"\b(?:[A-Za-z0-9+/]{40,}={0,2})\b")
POTENTIAL_KEY_RE = re.compile(r"\b(?:api[_-]?key|secret|access[_-]?token|auth[_-]?token)[\s:=]{1,3}['\"]?([A-Za-z0-9\-\._]{8,})['\"]?", re.IGNORECASE)
SUSPICIOUS_CMD_RE = re.compile(r"(su\b|mount\b|chmod\b|chown\b|rm\s+-rf\b|dd\b|mkfs\b)", re.IGNORECASE)

def scan_text_for_indicators(text: str) -> Dict[str, List[str]]:
    """Return a dict with found indicators grouped by type."""
    found = {
        "urls": [],
        "ips": [],
        "base64": [],
        "potential_keys": [],
        "suspicious_cmds": []
    }

    if not text:
        return found

    found["urls"] = list(dict.fromkeys(URL_RE.findall(text)))
    found["ips"] = list(dict.fromkeys(IP_RE.findall(text)))
    found["base64"] = list(dict.fromkeys(BASE64_RE.findall(text)))
    found["potential_keys"] = [m.group(0) for m in POTENTIAL_KEY_RE.finditer(text)]
    found["suspicious_cmds"] = list(dict.fromkeys(SUSPICIOUS_CMD_RE.findall(text)))

    # small normalization: remove empty items
    for k in found:
        found[k] = [x for x in found[k] if x]

    return found

def heuristic_risk_score(manifest: dict, indicators: dict) -> int:
    """
    Produce a simple heuristic risk score (0-100) based on:
     - dangerous permissions
     - presence of endpoints/IPs/commands/keys
    This is intentionally simple and transparent.
    """
    score = 0
    # permission weights (example)
    weight_map = {
        "android.permission.SEND_SMS": 15,
        "android.permission.RECEIVE_SMS": 12,
        "android.permission.READ_SMS": 12,
        "android.permission.WRITE_EXTERNAL_STORAGE": 8,
        "android.permission.READ_EXTERNAL_STORAGE": 8,
        "android.permission.INTERNET": 6,
        "android.permission.RECORD_AUDIO": 10,
        "android.permission.CAMERA": 8,
        "android.permission.READ_CONTACTS": 10,
        "android.permission.WRITE_CONTACTS": 10,
        "android.permission.ACCESS_FINE_LOCATION": 10
    }

    for p in manifest.get("permissions", []):
        for key, w in weight_map.items():
            if key.lower() in p.lower():
                score += w

    # indicators
    if indicators.get("urls"):
        score += min(len(indicators["urls"]) * 6, 30)
    if indicators.get("ips"):
        score += min(len(indicators["ips"]) * 6, 24)
    if indicators.get("potential_keys"):
        score += min(len(indicators["potential_keys"]) * 10, 30)
    if indicators.get("suspicious_cmds"):
        score += min(len(indicators["suspicious_cmds"]) * 8, 32)
    if indicators.get("base64"):
        score += min(len(indicators["base64"]) * 4, 16)

    # clamp
    if score > 100:
        score = 100
    return int(score)