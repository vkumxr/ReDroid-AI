"""
analyzers/static_analyzer.py
Orchestrates static analysis: decoding APK, parsing manifest, scanning strings,
and producing JSON output suitable for AI ingestion.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any
from utils.file_utils import decode_apk_with_apktool, decompile_with_jadx, safe_read, list_files_recursive
from utils.manifest_parser import parse_manifest
from utils.string_scanner import scan_text_for_indicators, heuristic_risk_score

class StaticAnalyzer:
    def __init__(self, workspace: str = "workspace"):
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)

    def analyze(self, apk_path: str, decode_with_jadx: bool = False) -> Dict[str, Any]:
        apk_name = Path(apk_path).stem
        out_dir = str(self.workspace / apk_name)
        # Step 1: decode APK with apktool
        decode_apk_with_apktool(apk_path, out_dir)

        # Optional: decompile with jadx for richer string sources
        if decode_with_jadx:
            try:
                decompile_with_jadx(apk_path, out_dir)
            except Exception as e:
                # proceed even if jadx fails; jadx is optional
                print(f"[!] JADX warning: {e}")

        # Step 2: parse manifest
        manifest_file = Path(out_dir) / "AndroidManifest.xml"
        manifest_info = {}
        if manifest_file.exists():
            manifest_info = parse_manifest(str(manifest_file))
        else:
            print("[!] manifest not found after decode")

        # Step 3: gather textual sources to scan
        combined_text = ""

        # 3a: scan resources, smali, assets, res, etc.
        for candidate_dir in ["res", "smali", "smali_classes2", "assets", "lib"]:
            p = Path(out_dir) / candidate_dir
            if p.exists():
                for f in p.rglob("*"):
                    if f.is_file():
                        # only read reasonably sized files
                        if f.stat().st_size < 500_000:
                            combined_text += "\n" + safe_read(str(f))

        # 3b: if JADX output exists, scan it too
        jadx_src = Path(out_dir) / "jadx-src"
        if jadx_src.exists():
            for f in jadx_src.rglob("*.java"):
                if f.is_file() and f.stat().st_size < 300_000:
                    combined_text += "\n" + safe_read(str(f))

        # Step 4: run textual indicators scanner
        indicators = scan_text_for_indicators(combined_text)

        # Step 5: compute heuristic risk
        risk = heuristic_risk_score(manifest_info, indicators)

        # Step 6: file list snapshot
        files = list_files_recursive(out_dir)

        # Build final JSON-friendly report
        report = {
            "apk": str(Path(apk_path).name),
            "package": manifest_info.get("package"),
            "permissions": manifest_info.get("permissions", []),
            "activities": manifest_info.get("activities", []),
            "services": manifest_info.get("services", []),
            "receivers": manifest_info.get("receivers", []),
            "providers": manifest_info.get("providers", []),
            "intent_filters": manifest_info.get("intent_filters", []),
            "indicators": indicators,
            "file_snapshot": files,
            "risk_score": risk
        }
        return report

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Static analysis pipeline for Android APKs")
    parser.add_argument("apk", help="path to apk file")
    parser.add_argument("--workspace", default="workspace", help="output workspace dir")
    parser.add_argument("--jadx", action="store_true", help="also run jadx decompile")
    parser.add_argument("--out-json", help="path to write JSON report")
    args = parser.parse_args()

    analyzer = StaticAnalyzer(args.workspace)
    report = analyzer.analyze(args.apk, decode_with_jadx=args.jadx)
    json_text = json.dumps(report, indent=2)
    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as fh:
            fh.write(json_text)
        print(f"[+] Written JSON report to {args.out_json}")
    else:
        print(json_text)

if __name__ == "__main__":
    main()