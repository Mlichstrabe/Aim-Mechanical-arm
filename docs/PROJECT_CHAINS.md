# Project Chains

这份文档先抛开和 `needle_tracking` 的整合，只说明 `aimooe_ur5e` 自己的三条主线。

## 1. Aimooe 光学定位链路

目标：让 Aimooe 定位仪从原始 marker 点识别出工具位姿。

文件位置：

```text
src/aimooe_sdk/
  Demo.py
  demo1.py
  Aimooe_timo.py
  CollectedToolData.py
runtime/
  AimPosition.pyd
  libusb0.dll
  opencv_core2413.dll
  python39.dll
AimTools/
  PTM-4.aimtool
  PTM-99.aimtool
data/outputs/
  aimooe_tool_data/
  camera/
```

数据流：

```text
Aimooe hardware
  -> Aim_GetMarkerAndStatusFromHardware()
  -> marker points: MarkerNumber, MarkerCoordinate
  -> Aim_FindToolInfo()
  -> tool pose: OriginCoor, Rto, tooltip
  -> CSV or console output
```

你读这条链路时重点看四个概念：

- `MarkerCoordinate`：定位仪直接看到的反光点坐标。
- `.aimtool`：定义某个工具由哪些 marker 组成。
- `OriginCoor` / `Rto`：工具坐标系在光学坐标系下的位置和姿态。
- `tooltip`：工具尖端位置，穿刺任务里通常比工具原点更关键。

推荐阅读顺序：

1. `docs/AIMOOE_OUTPUT_FIELDS.md`
2. `src/aimooe_sdk/Aimooe_timo.py`
3. `src/aimooe_sdk/CollectedToolData.py`
4. `src/aimooe_sdk/Demo.py` 或 `src/aimooe_sdk/demo1.py`

## 2. UR5e 机器人控制链路

目标：通过 UR RTDE 接口连接 UR5e，读取机器人状态并发送运动命令。

文件位置：

```text
src/ur5e_control/
  Init.py
```

当前真实代码流：

```text
ROBOT_IP
  -> RTDEControlInterface(robot_ip)
  -> RTDEReceiveInterface(robot_ip)
  -> getActualQ()
  -> moveJ(START_POINT_RADIANS)
  -> disconnect()
```

当前包含：

- `Init.py`：关节空间回初始位姿
- `execute_ct_puncture.py`：读取 CT 穿刺计划 + 标定链，默认 dry-run，可选 `--execute` 真机 moveL

后续 PBVS 或力控脚本应继续放在 `src/ur5e_control/`；历史实验日志在 `data/experiments/`。

硬件运行前必须确认：

- `ROBOT_IP` 是否正确。
- 机器人工作空间是否安全。
- 急停是否可用。
- `velocity` 和 `acceleration` 是否足够保守。
- 当前脚本是 `moveJ` 关节空间运动，不是沿直线到穿刺点的 `moveL`。

## 3. 离线理解与坐标变换链路

目标：没有 Aimooe 和 UR5e 时，先把“规划点如何变成机器人目标点”这件事跑通。

文件位置：

```text
run_offline_demo.py
src/offline_bridge/
  io.py
  transforms.py
  coord_bridge.py
  mock_robot.py
data/sample/
  calibration_chain.json
  puncture_plan.json
  tool_pose_frame.json
data/calibration/
  calibration_chain.json
  HandEye_Calibration_Matrix.npz   # when available
  space_reg.npz                    # when available
tests/
  test_offline_bridge.py
  test_coord_bridge.py
```

数据流：

```text
data/sample/puncture_plan.json
  -> entry / target in ct_scene_mm

data/sample/calibration_chain.json
  -> ct_to_optical
  -> optical_to_robot

src/offline_bridge/transforms.py
  -> compose_transform(optical_to_robot, ct_to_optical)
  -> apply_transform(ct_to_robot, entry)
  -> apply_transform(ct_to_robot, target)

src/offline_bridge/mock_robot.py
  -> MockRobot.move_l(entry_robot_mm)
```

这条链路的核心公式：

```text
p_out = R @ p_in + t
```

当前离线样例使用的坐标链：

```text
ct_scene_mm -> optical_mm -> robot_base_mm
```

推荐你先读这条链路，因为它不依赖硬件、最容易测试，也最能解释项目为什么需要标定矩阵。

运行：

```powershell
python run_offline_demo.py
python -m unittest tests.test_offline_bridge
```

## What Is Not Mainline

`archive/unrelated_dict/` 是词典/英语学习相关内容，不属于 UR5e/Aimooe 项目主线。

`data/experiments/` 用来放实验日志和结果。它不是入口代码，阅读时先不要从这里开始。
