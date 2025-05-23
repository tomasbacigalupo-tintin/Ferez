"""Utilities for checking and applying software updates."""

from __future__ import annotations
import zipfile
from distutils.version import LooseVersion
from pathlib import Path
from typing import Optional, Tuple

import requests


def check_for_updates(metadata_url: str, current_version: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """Check a remote JSON metadata file for updates.

    The metadata should contain ``{"version": "x.y.z", "url": "http://..."}``.
    Returns a tuple ``(available, version, url)``.
    """

    try:
        resp = requests.get(metadata_url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        version = data.get("version")
        package_url = data.get("url")
        if version and package_url and LooseVersion(version) > LooseVersion(current_version):
            return True, version, package_url
    except Exception:
        pass
    return False, None, None


def download_package(url: str, dest: Path) -> Path:
    """Download the update package to *dest* and return the file path."""

    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=10) as resp:
        resp.raise_for_status()
        with dest.open("wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
    return dest


def apply_update(package_path: Path, target_dir: Path) -> bool:
    """Extract the zip package into *target_dir*."""

    target_dir = Path(target_dir)
    try:
        with zipfile.ZipFile(package_path, "r") as zf:
            zf.extractall(target_dir)
        return True
    except Exception:
        return False


def update(metadata_url: str, current_version: str, install_dir: Path) -> bool:
    """Check for updates and apply them if available."""

    available, version, package_url = check_for_updates(metadata_url, current_version)
    if not available or not package_url:
        return False

    tmp_path = download_package(package_url, Path("update.zip"))
    return apply_update(tmp_path, install_dir)
