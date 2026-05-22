# aimooe_ur5e 与 needle_tracking 整合说明

本文档记录与独立项目 **needle_tracking（无配准版）** 的配准整合方案。

**外部项目路径：**

`C:\Users\Lu\PyCharmMiscProject\needle_tracking\needle_tracking 3-27-稳定备份\needle_tracking 无配准`

## 结论摘要

- needle_tracking：**CT 规划 + IMU 对准训练**，无 CT→患者/光学空间配准。
- aimooe_ur5e：提供 **L1 针尖注册、L2 手眼、L3 CT→光学**，并驱动 **UR5e**。
- 整合方式：补上 **CT → 光学 → 机器人** 变换链，而非合并两份无关矩阵。

## 坐标变换链

```
p_opt_mm  = R_ct2opt @ p_ct_mm + t_ct2opt    # L3，space_reg.npz
p_rob_mm  = R_opt2rob @ p_opt_mm + t_opt2rob # L2，HandEye_Calibration_Matrix.npz
```

执行目标（已确认）：机器人对准 **CT Entry** 经 L3→光学→手眼后的位置（与规划一致）。

## 分工

| 角色 | needle_tracking | aimooe_ur5e |
|------|-----------------|-------------|
| 术前规划 | DICOM 上选 Entry/Target | — |
| 空间配准 | 导出 `puncture_plan.json` | L3：`demo1.py` case 62 → `space_reg.npz` |
| 执行 | — | `execute_ct_puncture.py`（待实现）+ PBVS / 力控 |

## 待实现（aimooe_ur5e）

1. `hand–eye calibration/calibration/` 统一存放 NPZ/JSON
2. `collect_space_reg.py`、`coord_bridge.py`
3. `execute_ct_puncture.py`：读 plan + 标定 → moveL / PBVS

## 待实现（needle_tracking）

1. 穿刺点确认后导出 `puncture_plan.json`（`coord_frame: ct_scene_mm`）
2. 不内嵌 AimPosition，避免与 PyQt 进程冲突

## 标定顺序

1. L1：`Demo.py` 针尖注册 → `PTM-4.aimtool`
2. L2：同步采集 + `手眼标定最终.py`
3. L3：四点 fiducial → `space_reg.npz`
4. 同一套 DICOM 在 needle_tracking 选 Entry 并导出 plan
5. aimooe 低速验证 Entry 上方约 20 mm

## 环境变量

- `AIMOOE_CALIB_DIR`：指向共享 `calibration/` 目录（可选）
