import unittest

from src.offline_bridge.mock_robot import MockRobot
from src.offline_bridge.transforms import (
    apply_transform,
    compose_transform,
    transform_plan_ct_to_robot,
)


class TransformTests(unittest.TestCase):
    def test_apply_transform_rotates_and_translates_point(self):
        transform = {
            "from": "ct_scene_mm",
            "to": "optical_mm",
            "R": [
                [0.0, -1.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0],
            ],
            "t": [10.0, 20.0, 30.0],
        }

        self.assertEqual(apply_transform(transform, [1.0, 2.0, 3.0]), [8.0, 21.0, 33.0])

    def test_compose_transform_preserves_source_and_target_frames(self):
        ct_to_optical = {
            "from": "ct_scene_mm",
            "to": "optical_mm",
            "R": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            "t": [100.0, 0.0, 0.0],
        }
        optical_to_robot = {
            "from": "optical_mm",
            "to": "robot_base_mm",
            "R": [[1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]],
            "t": [0.0, 10.0, 0.0],
        }

        composed = compose_transform(optical_to_robot, ct_to_optical)

        self.assertEqual(composed["from"], "ct_scene_mm")
        self.assertEqual(composed["to"], "robot_base_mm")
        self.assertEqual(apply_transform(composed, [1.0, 2.0, 3.0]), [101.0, 7.0, 2.0])

    def test_transform_plan_ct_to_robot_outputs_entry_and_target(self):
        plan = {"entry": [1.0, 2.0, 3.0], "target": [4.0, 5.0, 6.0]}
        ct_to_optical = {
            "from": "ct_scene_mm",
            "to": "optical_mm",
            "R": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            "t": [10.0, 0.0, 0.0],
        }
        optical_to_robot = {
            "from": "optical_mm",
            "to": "robot_base_mm",
            "R": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            "t": [0.0, 20.0, 0.0],
        }

        transformed = transform_plan_ct_to_robot(plan, ct_to_optical, optical_to_robot)

        self.assertEqual(transformed["frame"], "robot_base_mm")
        self.assertEqual(transformed["entry"], [11.0, 22.0, 3.0])
        self.assertEqual(transformed["target"], [14.0, 25.0, 6.0])


class MockRobotTests(unittest.TestCase):
    def test_mock_robot_records_move_l_without_hardware(self):
        robot = MockRobot()

        command = robot.move_l([100.0, 200.0, 300.0], speed=20.0, acceleration=50.0)

        self.assertEqual(command["command"], "moveL")
        self.assertEqual(command["target_mm"], [100.0, 200.0, 300.0])
        self.assertEqual(robot.commands, [command])


if __name__ == "__main__":
    unittest.main()
