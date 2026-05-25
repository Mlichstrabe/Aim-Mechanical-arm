# aimooe_ur5e 离线接手路线

这份路线适合设备暂时不在身边的阶段。核心方法是：先读代码和文档，再用假数据跑通最小链路，最后等定位仪和 UR5e 到手后做低速验证。

如果你想每天照着执行，使用更细的 30 天版本：`docs/DAILY_STUDY_PLAN.md`。

## 一个月目标

到第 4 周结束时，你应该能做到：

- 说清 Aimooe 定位仪输出的 marker、tool、`OriginCoor`、`Rto`、`tooltip` 是什么。
- 说清 `CT -> optical -> robot` 坐标链路，每个矩阵从哪个坐标系变到哪个坐标系。
- 看懂 `src/ur5e_control/Init.py` 中 UR5e RTDE 的连接和 `moveJ` 初始化动作。
- 不接设备也能运行离线 demo，完成“假定位仪/规划数据 -> 坐标转换 -> mock 机器人命令”。

## 第 1 周：定位仪代码

重点文件：

- `src/aimooe_sdk/Demo.py` / `src/aimooe_sdk/demo1.py`：Aimooe SDK 原始 demo，重点看 case 60 和 case 62。
- `src/aimooe_sdk/Aimooe_timo.py`：PTM-99 专用工具数据采集。
- `src/aimooe_sdk/CollectedToolData.py`：更完整的工具字段采集。

要学会的问题：

- marker 点和 tool 的区别是什么。
- `Aim_FindToolInfo` 如何把一组 marker 匹配成工具。
- `OriginCoor`、`Rto`、`tooltip` 分别代表什么。
- case 62 空间配准为什么对应 `CT -> optical`。

离线练习：

```powershell
python run_offline_demo.py
```

然后打开 `data/sample/tool_pose_frame.json`，对照 `docs/AIMOOE_OUTPUT_FIELDS.md` 逐项解释字段。

## 第 2 周：坐标系和标定

重点文件：

- `docs/INTEGRATION_NEEDLE_TRACKING.md`
- `src/offline_bridge/transforms.py`
- `data/sample/calibration_chain.json`
- `data/sample/puncture_plan.json`

要学会的问题：

- 为什么 3D 点变换可以写成 `p_out = R @ p_in + t`。
- 为什么项目里必须记录矩阵的 `from` 和 `to`，不能只保存数字。
- `CT -> optical -> robot` 中任何一步方向写反会造成什么后果。
- 手眼标定 AX=XB 在这里解决的是 `optical -> robot` 或工具/末端之间的关系。

离线练习：

```powershell
python -m unittest tests.test_offline_bridge
```

然后手算 `tests/test_offline_bridge.py` 里的第一个点变换，确认代码结果和手算一致。

## 第 3 周：UR5e 控制接口

重点文件：

- `src/ur5e_control/Init.py`
- `src/offline_bridge/mock_robot.py`

要学会的问题：

- `rtde_control.RTDEControlInterface` 和 `rtde_receive.RTDEReceiveInterface` 分别负责什么。
- `moveJ` 是关节空间运动，后续执行穿刺点附近对准通常会用 `moveL` 或更细的伺服控制。
- `ROBOT_IP`、速度、加速度为什么不能随意改。
- 没有设备时，为什么要用 mock robot 先检查目标点和单位。

离线练习：

- 改 `data/sample/puncture_plan.json` 里的 `entry`，重新运行 `run_offline_demo.py`。
- 确认 mock robot 输出的 `target_mm` 只变化在你预期的方向。

## 第 4 周：最小闭环

目标链路：

```text
puncture_plan.json
  -> CT entry/target
  -> ct_to_optical
  -> optical_to_robot
  -> robot_base_mm entry/target
  -> MockRobot.move_l()
```

当前离线实现对应三个模块：

- 定位仪/规划输入：`data/sample/*.json`
- 坐标转换：`src/offline_bridge/transforms.py`
- 机器人执行替身：`src/offline_bridge/mock_robot.py`

设备到手前不要急着接 ROS2。先把这条 Python 链路讲清楚、测清楚。ROS2 后续只是把这些输入输出变成 topic、service 和 `tf2`。

## 设备到手后的第一轮验证

1. 只接 Aimooe，运行原始 demo，确认 marker 数量和 tool 姿态稳定。
2. 只接 UR5e，读取当前关节/TCP 状态，不移动。
3. 低速运行 `src/ur5e_control/Init.py` 前，先确认 IP、安全空间、急停和速度。
4. 只移动到 Entry 上方安全距离，不直接做穿刺、PBVS 或力控。
