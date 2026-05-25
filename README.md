# aimooe_ur5e

UR5e robotic-arm experiment workspace with Aimooe optical tracking support.

这个仓库现在按“阅读和接手项目”重新整理过。先不要把它理解成完整 ROS 工程；当前真实代码更像一个机械臂实验工作台，核心围绕三条链路：

1. Aimooe 光学定位链路
2. UR5e 机器人控制链路
3. 离线理解与坐标变换链路

详细逻辑见 [docs/PROJECT_CHAINS.md](docs/PROJECT_CHAINS.md)。

## Directory Layout

```text
aimooe_ur5e/
  README.md
  environment.yml
  run_offline_demo.py

  src/
    aimooe_sdk/          # Aimooe SDK demos and tool-pose collection scripts
    ur5e_control/        # UR5e RTDE entry scripts
    offline_bridge/      # No-hardware coordinate-transform learning flow

  runtime/               # Local Aimooe binary runtime files (AimPosition.pyd, DLLs)
  AimTools/              # PTM-4 / PTM-99 .aimtool files (see AimTools/README.md)
  scripts/
    check_env.py         # Verify Python 3.9, runtime DLLs, tool files

  data/
    sample/              # Small JSON examples for the offline flow
    calibration/         # HandEye / space_reg NPZ and calibration_chain.json
    outputs/             # aimooe_tool_data/, camera/ (runtime CSV and images)
    experiments/         # Historical logs and figures (not entry code)

  docs/                  # Reading guides and project notes
  tests/                 # Offline tests
  archive/               # Unrelated or historical material kept out of the main path
```

## Quick Start Without Hardware

Run the offline chain first:

```powershell
python run_offline_demo.py
python -m unittest discover -s tests -q
python src/ur5e_control/execute_ct_puncture.py --sample-calibration
```

Expected behavior:

- read a sample CT-style puncture plan from `data/sample/puncture_plan.json`
- read calibration transforms from `data/sample/calibration_chain.json`
- convert entry/target points into `robot_base_mm`
- send the entry point to `MockRobot.move_l()` without touching real hardware

## Hardware Entry Points

Check environment first (Python 3.9, DLLs, `.aimtool` files):

```powershell
conda activate aimooe-ur5e
python scripts/check_env.py
```

Copy `PTM-4.aimtool` and `PTM-99.aimtool` into `AimTools/` before optical scripts (see `AimTools/README.md`).

Aimooe SDK scripts:

```powershell
python src/aimooe_sdk/Demo.py
python src/aimooe_sdk/demo1.py
python src/aimooe_sdk/Aimooe_timo.py
python src/aimooe_sdk/CollectedToolData.py
```

UR5e:

```powershell
python src/ur5e_control/Init.py
python src/ur5e_control/execute_ct_puncture.py --sample-calibration
```

Before running hardware code, check the robot IP, emergency stop, workspace clearance, speed, acceleration, and whether the Aimooe runtime files in `runtime/` match Python 3.9.

## Migrated from the old flat layout?

If you still have root folders from before the restructure (`datatimo/`, `datamark/`, `data_tcp/`, `hand-eye calibration/`, `Aimtools/`):

```powershell
python scripts/migrate_legacy_layout.py --dry-run
python scripts/migrate_legacy_layout.py
python scripts/create_legacy_links.py
```

Old entry commands still work via root launchers: `python Init.py`, `python Demo.py`, `python Aimooe_timo.py`.

## Environment

Recommended:

- Windows
- Python 3.9 for the Aimooe binary extension
- UR5e with RTDE enabled
- Aimooe optical tracker and matching `.aimtool` files

Conda setup:

```powershell
conda env create -f environment.yml
conda activate aimooe-ur5e
```

## Notes

- `runtime/` contains local binary files used by Aimooe scripts (requires **Python 3.9**).
- `AimTools/` is required for tool tracking; `.aimtool` files are not stored in git—copy from your Aimooe installation.
- `data/calibration/` holds `HandEye_Calibration_Matrix.npz` and `space_reg.npz` when available.
- `archive/unrelated_dict/` is not part of the robotic-arm project.
- Some older Chinese comments in inherited SDK scripts may display as mojibake in terminals with the wrong encoding. The new docs use UTF-8.
