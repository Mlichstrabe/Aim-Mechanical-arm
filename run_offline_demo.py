"""Run the no-hardware Aimooe -> transform -> mock UR5e learning flow."""

from __future__ import annotations

from pathlib import Path

from src.offline_bridge.io import load_json
from src.offline_bridge.mock_robot import MockRobot
from src.offline_bridge.transforms import transform_plan_ct_to_robot


ROOT = Path(__file__).resolve().parent


def main() -> None:
    sample_dir = ROOT / "data" / "sample"
    calibration = load_json(sample_dir / "calibration_chain.json")
    plan = load_json(sample_dir / "puncture_plan.json")
    tool_pose = load_json(sample_dir / "tool_pose_frame.json")

    transformed_plan = transform_plan_ct_to_robot(
        plan,
        calibration["ct_to_optical"],
        calibration["optical_to_robot"],
    )
    robot = MockRobot()
    command = robot.move_l(transformed_plan["entry"], speed=20.0, acceleration=50.0)

    print("Offline Aimooe frame:")
    print(f"  tool={tool_pose['tool_name']} origin_mm={tool_pose['OriginCoor']}")
    print("Transformed puncture plan:")
    print(f"  entry_robot_mm={transformed_plan['entry']}")
    print(f"  target_robot_mm={transformed_plan['target']}")
    print("Mock robot command:")
    print(f"  {command}")


if __name__ == "__main__":
    main()
