"""Reminder entry for L3 CT->optical registration (implemented in demo1.py case 62)."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.project_paths import CALIBRATION_DIR


def main() -> None:
    print("L3 space registration is performed inside demo1.py menu case 62.")
    print("Steps:")
    print("  1. conda activate aimooe-ur5e")
    print("  2. python src/aimooe_sdk/demo1.py")
    print("  3. Choose case 62 and follow on-screen fiducial capture")
    print(f"  4. Copy the exported NPZ to: {CALIBRATION_DIR / 'space_reg.npz'}")
    print("Expected NPZ keys: R_ct2opt, t_ct2opt (mm).")
    print("See data/calibration/README.md and docs/INTEGRATION_NEEDLE_TRACKING.md.")


if __name__ == "__main__":
    main()
