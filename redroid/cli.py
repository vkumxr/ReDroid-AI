import sys
from redroid.core.unpack import unpack_apk, APKUnpackError


def main():
    if len(sys.argv) != 2:
        print("Usage: redroid <path_to_apk>")
        sys.exit(1)

    apk_path = sys.argv[1]

    try:
        extracted_path = unpack_apk(apk_path)
        print(f"[+] APK unpacked to: {extracted_path}")

    except APKUnpackError as e:
        print(f"[!] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
