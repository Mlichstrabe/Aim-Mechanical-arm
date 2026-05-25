"""Execute a CT puncture plan on UR5e after L2/L3 calibration (dry-run by default)."""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.offline_bridge.coord_bridge import load_calibration_chain, transform_plan_ct_to_robot
from src.offline_bridge.io import load_json
from src.offline_bridge.mock_robot import MockRobot
from src.project_paths import SAMPLE_DIR


def _pose6_from_xyz_mm(xyz_mm: list[float], rx: float = math.pi, ry: float = 0.0, rz: float = 0.0) -> list[float]:
    """Build UR pose [x,y,z,rx,ry,rz] with positions in meters."""
    x, y, z = xyz_mm
    return [x / 1000.0, y / 1000.0, z / 1000.0, rx, ry, rz]


def main() -> None:
    parser = argparse.ArgumentParser(description="CT plan -> robot base (optional UR5e moveL).")
    parser.add_argument(
        "--plan",
        type=Path,
        default=SAMPLE_DIR / "puncture_plan.json",
        help="Puncture plan JSON (coord_frame: ct_scene_mm).",
    )
    parser.add_argument(
        "--sample-calibration",
        action="store_true",
        help="Use data/sample/calibration_chain.json instead of data/calibration/.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Connect to UR5e and moveL to approach pose (default: dry-run only).",
    )
    parser.add_argument("--robot-ip", default="192.168.56.101")
    parser.add_argument("--offset-above-mm", type=float, default=20.0, help="Approach offset along +Z in robot base.")
    args = parser.parse_args()

    plan = load_json(args.plan)
    if args.sample_calibration:
        from src.offline_bridge.coord_bridge import load_sample_calibration_chain

        chain = load_sample_calibration_chain()
    else:
        chain = load_calibration_chain()

    transformed = transform_plan_ct_to_robot(plan, chain)
    entry = transformed["entry"]
    approach = [entry[0], entry[1], entry[2] + args.offset_above_mm]

    print("Transformed plan (robot_base_mm):")
    print(f"  entry : {[round(v, 3) for v in entry]}")
    print(f"  target: {[round(v, 3) for v in transformed['target']]}")
    print(f"  approach (+{args.offset_above_mm} mm Z): {[round(v, 3) for v in approach]}")

    if not args.execute:
        cmd = MockRobot().move_l(approach, speed=20.0, acceleration=50.0)
        print("Dry-run mock command:", cmd)
        return

    import rtde_control

    pose = _pose6_from_xyz_mm(approach)
    rtde_c = rtde_control.RTDEControlInterface(args.robot_ip)
    try:
        print("Executing moveL to approach pose (m, rad):", [round(v, 6) for v in pose])
        rtde_c.moveL(pose, speed=0.05, acceleration=0.1)
        print("Done.")
    finally:
        rtde_c.disconnect()


if __name__ == "__main__":
    main()
