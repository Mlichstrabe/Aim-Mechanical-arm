import unittest

from src.offline_bridge.coord_bridge import (
    load_sample_calibration_chain,
    transform_ct_point_to_robot,
    transform_plan_ct_to_robot,
)
from src.offline_bridge.io import load_json
from src.project_paths import SAMPLE_DIR


class CoordBridgeTests(unittest.TestCase):
    def test_transform_ct_point_matches_offline_demo(self):
        chain = load_sample_calibration_chain()
        plan = load_json(SAMPLE_DIR / "puncture_plan.json")
        transformed = transform_plan_ct_to_robot(plan, chain)
        entry = transform_ct_point_to_robot(chain, plan["entry"])
        self.assertEqual(entry, transformed["entry"])
        self.assertEqual(transformed["frame"], "robot_base_mm")


if __name__ == "__main__":
    unittest.main()
