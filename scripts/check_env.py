"""Verify Python version, runtime binaries, and AimTools layout."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.project_paths import (
    RUNTIME_DIR,
    list_missing_aimtools,
    resolve_aimtools_dir,
)


def main() -> int:
    ok = True
    print(f"Repository root: {_REPO_ROOT}")
    print(f"Python: {sys.version.split()[0]} (need 3.9.x for AimPosition.pyd)")

    if sys.version_info[:2] != (3, 9):
        print("  [FAIL] Use: conda activate aimooe-ur5e")
        ok = False
    else:
        print("  [OK]")

    pyd = RUNTIME_DIR / "AimPosition.pyd"
    print(f"Runtime: {RUNTIME_DIR}")
    for name in ("AimPosition.pyd", "libusb0.dll", "opencv_core2413.dll", "python39.dll"):
        path = RUNTIME_DIR / name
        status = "OK" if path.is_file() else "MISSING"
        print(f"  [{status}] {name}")
        if not path.is_file():
            ok = False

    print(f"AimTools: {resolve_aimtools_dir()}")
    missing = list_missing_aimtools()
    if missing:
        print("  [FAIL] Missing:", ", ".join(missing))
        print("  See AimTools/README.md")
        ok = False
    else:
        print("  [OK] PTM-4.aimtool, PTM-99.aimtool")

    if ok and sys.version_info[:2] == (3, 9):
        try:
            from src.aimooe_sdk.runtime_path import configure_runtime_path, require_python39

            configure_runtime_path()
            require_python39()
            import AimPosition  # noqa: F401

            print("  [OK] AimPosition import")
        except Exception as exc:
            print(f"  [FAIL] AimPosition import: {exc}")
            ok = False

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
