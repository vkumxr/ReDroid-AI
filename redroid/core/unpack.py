from pathlib import Path
import zipfile
import tempfile


class APKUnpackError(Exception):
    pass


def unpack_apk(apk_path: str) -> Path:
    apk = Path(apk_path)

    if not apk.exists():
        raise APKUnpackError(f"APK not found: {apk}")

    if apk.suffix.lower() != ".apk":
        raise APKUnpackError("Input file is not an APK")

    try:
        tmp_dir = Path(tempfile.mkdtemp(prefix="redroid_apk_"))

        with zipfile.ZipFile(apk, "r") as z:
            z.extractall(tmp_dir)

        return tmp_dir

    except zipfile.BadZipFile:
        raise APKUnpackError("Invalid or corrupted APK")
