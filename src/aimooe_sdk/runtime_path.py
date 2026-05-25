"""Runtime path setup for the local Aimooe SDK extension files."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.project_paths import (
    AIMOOE_OUTPUT_DIR,
    AIMTOOLS_CANONICAL,
    CAMERA_OUTPUT_DIR,
    CALIBRATION_DIR,
    ROOT,
    RUNTIME_DIR,
    aimtools_path,
    ensure_dir,
    legacy_datatimo_dir,
    list_missing_aimtools,
    resolve_aimtools_dir,
)

AIMTOOLS_DIR = AIMTOOLS_CANONICAL

__all__ = [
    "ROOT",
    "RUNTIME_DIR",
    "AIMTOOLS_DIR",
    "CALIBRATION_DIR",
    "AIMOOE_OUTPUT_DIR",
    "CAMERA_OUTPUT_DIR",
    "aimtools_path",
    "aimooe_output_dir",
    "camera_output_dir",
    "calibration_dir",
    "configure_runtime_path",
    "require_python39",
    "require_aimtools",
]


def configure_runtime_path() -> None:
    runtime = str(RUNTIME_DIR)
    if runtime not in sys.path:
        sys.path.insert(0, runtime)
    if hasattr(os, "add_dll_directory") and RUNTIME_DIR.exists():
        os.add_dll_directory(runtime)


def aimooe_output_dir() -> str:
    return str(legacy_datatimo_dir())


def camera_output_dir() -> str:
    return str(ensure_dir(CAMERA_OUTPUT_DIR))


def calibration_dir() -> str:
    return str(ensure_dir(CALIBRATION_DIR))


def require_python39() -> None:
    if sys.version_info[:2] != (3, 9):
        raise RuntimeError(
            "AimPosition.pyd requires Python 3.9. "
            f"Current interpreter: {sys.version.split()[0]}. "
            "Create the env with: conda env create -f environment.yml && conda activate aimooe-ur5e"
        )


def require_aimtools(required: tuple[str, ...] = ("PTM-4.aimtool", "PTM-99.aimtool")) -> None:
    missing = list_missing_aimtools(required)
    if missing:
        tools_dir = resolve_aimtools_dir()
        raise FileNotFoundError(
            "Missing Aimooe tool files: " + ", ".join(missing) + "\n"
            f"Checked directory: {tools_dir}\n"
            "Copy .aimtool files into AimTools/ (see AimTools/README.md)."
        )


def boot_sdk(*, check_tools: bool = True) -> None:
    """Configure DLL paths, verify Python 3.9, optionally verify tool files."""
    configure_runtime_path()
    require_python39()
    ensure_dir(resolve_aimtools_dir())
    if check_tools:
        require_aimtools()
