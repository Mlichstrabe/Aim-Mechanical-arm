# Offline Demo

`run_offline_demo.py` is the no-hardware learning entry point.

It does not connect to Aimooe or UR5e. It only reads sample files, converts coordinates, and records a mock robot command.

## Run

```powershell
python run_offline_demo.py
```

Expected output includes:

- a sample Aimooe tool frame from `data/sample/tool_pose_frame.json`
- transformed entry/target points from `data/sample/puncture_plan.json`
- a mock `moveL` command from `src/offline_bridge/mock_robot.py`

## File Flow

```text
data/sample/puncture_plan.json
data/sample/calibration_chain.json
  -> src/offline_bridge/transforms.py
  -> robot_base_mm entry/target
  -> src/offline_bridge/mock_robot.py
```

## Test

```powershell
python -m unittest tests.test_offline_bridge
```
