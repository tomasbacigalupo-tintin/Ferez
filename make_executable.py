#!/usr/bin/env python3
"""Builds a standalone executable using PyInstaller."""
import subprocess
import shutil
import sys


def main():
    pyinstaller_path = shutil.which("pyinstaller")
    if not pyinstaller_path:
        print("PyInstaller no está instalado. Instálalo con `pip install pyinstaller`.")
        sys.exit(1)

    cmd = [pyinstaller_path, "--onefile", "wifi_fix_tool.py"]
    try:
        result = subprocess.run(cmd, check=False)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()
