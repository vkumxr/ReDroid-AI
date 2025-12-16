from pathlib import Path
from redroid.core.unpack import unpack_apk, APKUnpackError


def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: redroid <apk_path>")
        return

    apk_path = sys.argv[1]

    try:
        decoded_path = unpack_apk(Path(apk_path))
        print(f"[+] APK decoded to: {decoded_path}")

    except APKUnpackError as e:
        print(f"[!] Error: {e}")


if __name__ == "__main__":
    main()
