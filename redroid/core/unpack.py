from pathlib import Path
import subprocess
import tempfile


class APKUnpackError(Exception):
    pass


def unpack_apk(apk_path: Path) -> Path:
    out_dir = Path(tempfile.mkdtemp(prefix="redroid_decoded_"))

    try:
        subprocess.run(
            ["apktool", "d", "-f", apk_path, "-o", out_dir],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return out_dir

    except Exception:
        raise APKUnpackError("apktool failed to decode APK")
