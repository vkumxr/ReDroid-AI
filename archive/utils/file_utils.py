"""
utils/file_utils.py
Helpers for filesystem tasks and invoking apktool/jadx.
"""
import os
import shutil
import subprocess
from pathlib import Path
from typing import Tuple

APKTOOL_CMD = "apktool"  # assume in PATH
JADX_CMD = "jadx"        # assume in PATH

def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

def run_cmd(cmd: list, cwd: str | None = None, capture_output: bool = False) -> Tuple[int, str, str]:
    """Run a system command and return (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=capture_output, text=True, check=False)
        return proc.returncode, proc.stdout if capture_output else "", proc.stderr if capture_output else ""
    except FileNotFoundError as e:
        return 127, "", str(e)

def decode_apk_with_apktool(apk_path: str, out_dir: str) -> bool:
    """
    Use apktool to decode an APK into a directory.
    Returns True on success.
    """
    ensure_dir(out_dir)
    cmd = [APKTOOL_CMD, "d", "-f", "-o", out_dir, apk_path]
    rc, out, err = run_cmd(cmd, capture_output=True)
    if rc != 0:
        raise RuntimeError(f"apktool failed: rc={rc}, err={err.strip()}")
    return True

def decompile_with_jadx(apk_path: str, out_dir: str) -> bool:
    """
    Use jadx to decompile Java/Kotlin sources (optional).
    It writes decompiled files into out_dir/jadx-src
    """
    target = Path(out_dir) / "jadx-src"
    ensure_dir(str(target))
    cmd = [JADX_CMD, "-d", str(target), apk_path]
    rc, out, err = run_cmd(cmd, capture_output=True)
    if rc != 0:
        # jadx sometimes returns non-zero on partial failures; raise only if critical
        raise RuntimeError(f"jadx failed: rc={rc}, err={err.strip()}")
    return True

def safe_read(path: str) -> str:
    """Read a file and return str. Return empty string on error."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""

def list_files_recursive(root: str) -> list:
    """Return list of file paths under root (relative)."""
    files = []
    for p in Path(root).rglob("*"):
        if p.is_file():
            files.append(str(p.relative_to(root)))
    return files