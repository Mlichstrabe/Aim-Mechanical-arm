# aimooe_ur5e 与 needle_tracking 整合说明

本文档记录与独立项目 **needle_tracking（无配准版）** 的配准整合方案。

**外部项目路径（示例）：**

`C:\Users\Lu\PyCharmMiscProject\needle_tracking\needle_tracking 3-27-稳定备份\needle_tracking 无配准`

## 结论摘要

- needle_tracking：**CT 规划 + IMU 对准训练**，无 CT→患者/光学空间配准。
- aimooe_ur5e：提供 **L1 针尖注册、L2 手眼、L3 CT→光学**，并驱动 **UR5e**。
- 整合方式：补上 **CT → 光学 → 机器人** 变换链，而非合并两份无关矩阵。

## 坐标变换链

```
p_opt_mm  = R_ct2opt @ p_ct_mm + t_ct2opt    # L3，data/calibration/space_reg.npz
p_rob_mm  = R_opt2rob @ p_opt_mm + t_opt2rob # L2，data/calibration/HandEye_Calibration_Matrix.npz
```

执行目标：机器人对准 **CT Entry** 经 L3→光学→手眼后的位置（与规划一致）。

实现代码：`src/offline_bridge/coord_bridge.py`、`src/ur5e_control/execute_ct_puncture.py`。

## 分工

| 角色 | needle_tracking | aimooe_ur5e |
|------|-----------------|-------------|
| 术前规划 | DICOM 上选 Entry/Target | — |
| 空间配准 | 导出 `puncture_plan.json` | L3：`src/aimooe_sdk/demo1.py` case 62 → `data/calibration/space_reg.npz` |
| 执行 | — | `src/ur5e_control/execute_ct_puncture.py` + 后续 PBVS / 力控（实验脚本见 `data/experiments/`） |

## 仓库内路径（重组后）

| 用途 | 路径 |
|------|------|
| 标定矩阵与 JSON | `data/calibration/`（可用环境变量 `AIMOOE_CALIB_DIR` 覆盖） |
| 离线样例 | `data/sample/puncture_plan.json`、`calibration_chain.json` |
| Aimooe 工具文件 | `AimTools/PTM-4.aimtool`、`PTM-99.aimtool` |
| 工具采集 CSV | `data/outputs/aimooe_tool_data/` |
| 相机截图 | `data/outputs/camera/` |
| 历史实验数据 | `data/experiments/hand_eye/`、`data/experiments/force/` |

## 标定与执行命令

```powershell
conda activate aimooe-ur5e
python scripts/check_env.py

# L1：针尖注册 → 更新 AimTools/PTM-4.aimtool
python src/aimooe_sdk/Demo.py

# L3：空间配准说明
python src/aimooe_sdk/collect_space_reg.py
python src/aimooe_sdk/demo1.py   # 菜单 case 62

# 离线验证 CT→机器人（样例标定）
python src/ur5e_control/execute_ct_puncture.py --sample-calibration

# 使用 data/calibration/ 下真实 NPZ/JSON 后干跑
python src/ur5e_control/execute_ct_puncture.py

# 真机（确认安全后）
python src/ur5e_control/execute_ct_puncture.py --execute
```

## 待实现（needle_tracking 侧）

1. 穿刺点确认后导出 `puncture_plan.json`（`coord_frame: ct_scene_mm`）
2. 不内嵌 AimPosition，避免与 PyQt 进程冲突

## 标定顺序

1. L1：`src/aimooe_sdk/Demo.py` 针尖注册 → `AimTools/PTM-4.aimtool`
2. L2：多目标点同步采集 + 手眼求解 → `data/calibration/HandEye_Calibration_Matrix.npz`（历史流程脚本需从备份恢复或重写）
3. L3：四点 fiducial → `data/calibration/space_reg.npz`（`demo1.py` case 62）
4. 同一套 DICOM 在 needle_tracking 选 Entry 并导出 plan
5. `execute_ct_puncture.py` 低速验证 Entry 上方约 20 mm

## 环境变量

- `AIMOOE_CALIB_DIR`：指向标定目录（默认 `data/calibration/`）
