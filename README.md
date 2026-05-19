# aimooe_ur5e — UR5e 机器人实验平台

> UR5e robotic arm experimental platform with Aimooe optical tracking for hand-eye calibration, force-control puncture, and PBVS visual servoing research.

## 项目概述 / Overview

本项目围绕 **UR5e 六自由度协作机器人** 和 **Aimooe 光学定位仪**，开展手术穿刺机器人相关研究，涵盖手眼标定、力控穿刺、视觉伺服等方向。

**核心研究内容：**

- **手眼标定** (Hand-Eye Calibration) — 基于光学定位仪的机器人手眼标定，AX=XB 问题求解，精度验证与误差分析
- **力控穿刺** (Force-Control Puncture) — 阻抗控制、导纳控制、混合力控、MPC 等算法在穿刺实验中的应用
- **PBVS 视觉伺服** (Position-Based Visual Servoing) — 基于位置的视觉伺服控制与跟踪实验
- **光学定位** (Optical Tracking) — Aimooe 光学定位仪的二次开发与数据采集

## 仓库统计 / Stats

| 类型 Type | 数量 Count |
|-----------|-----------|
| Python 脚本 | 105 |
| NPZ 数据/矩阵 | 17 |
| CSV 实验数据 | 92 |
| PNG 结果图 | 119 |
| PDF 报告图 | 36 |

## 目录结构 / Layout

```
aimooe_ur5e/
├── Aimooe_timo.py                 # Aimooe 工具信息采集（PTM-99 专用精简版）
├── CollectedToolData.py           # 工具数据采集（完整版，含全字段 CSV 输出）
├── Demo.py / demo1.py             # Aimooe SDK 功能演示（激光、相机、标记点检测等）
├── Init.py                        # UR5e RTDE 初始位置移动
├── AimPosition.pyd                # Aimooe Python 扩展库
├── libusb0.dll / opencv_*.dll     # 运行时依赖库
├── Aimtools/                      # Aimooe 工具定义文件
│   ├── PTM-4.aimtool
│   └── PTM-99.aimtool
│
├── hand–eye calibration/          # 手眼标定相关（核心）
│   ├── 手眼标定最终.py            # 最终版手眼标定（鲁棒优化、离群剔除）
│   ├── 手眼标定.py                # 基础版手眼标定
│   ├── 手眼标定00.py              # 早期版本
│   ├── 手眼标定精度2mm.py         # 精度验证（2mm 标准）
│   ├── 手眼标定自动收敛.py        # 自动收敛迭代优化
│   ├── 标定矩阵封装.py            # 标定矩阵封装工具
│   ├── 机械臂多目标点运动*.py      # 多目标点运动规划
│   ├── 机械臂 TCP 数据采集*.py     # TCP 数据采集
│   ├── 四点定位.py / 多点精准定位*.py  # 定位算法
│   ├── 伺服跟踪体膜.py / 跟踪*.py  # 伺服跟踪
│   ├── 光学定位仪采集*.py          # 光学定位仪数据采集
│   ├── 坐标变换.py / 变换矩阵保存*.py
│   ├── pbvs_experiment_data/       # PBVS 实验数据分析
│   ├── *.npz                       # 标定矩阵、位姿数据
│   ├── *.csv                       # 标定结果表格
│   ├── *.pdf                       # 误差分析、点云分布等报告图
│   └── calibration_results/        # 标定结果存档
│
├── force/                          # 力控实验（核心）
│   ├── 导纳控制.py                # 笛卡尔导纳控制（两态状态机，TCP 坐标系）
│   ├── 导纳控制250hz.py           # 250Hz 高频导纳控制
│   ├── 阻抗控制250hz.py           # 250Hz 高频阻抗控制
│   ├── 阻抗导纳融合力控.py        # 阻抗-导纳融合控制
│   ├── 混合力控带角度穿刺*.py      # 混合力控 + 角度穿刺
│   ├── 改进阻抗穿刺_MPC.py        # 改进阻抗 + MPC 穿刺
│   ├── 阻抗mpc算法.py / mpc算法.py # MPC 控制算法
│   ├── 顺应控制调参.py            # 顺应性参数整定
│   ├── 力控数据采集.py            # 力控实验数据采集
│   ├── 呼吸补偿的效果.py          # 呼吸运动补偿
│   ├── 零力标定*.py               # 力传感器零点标定
│   ├── ur5e正逆运动学*.py         # UR5e 正/逆运动学验证
│   ├── ur5e力控接口*.py           # UR5e 力控接口封装
│   ├── common_depth_window_force_plot_portable.py  # 力控结果综合绘图
│   ├── *.csv                       # 各实验日志（导纳、阻抗、混合、MPC）
│   ├── *.png                       # 力控结果对比图
│   └── force_calib_final/          # 力控标定结果
│
├── datatimo/                       # Aimooe 工具信息采集 CSV
├── datatp/                         # 标定转换结果
└── .gitignore
```

## 环境配置 / Environment

**推荐运行环境：**

- **操作系统：** Windows
- **Python：** 3.9（与 `python39.dll` 匹配）
- **硬件：** UR5e 协作机器人 + Aimooe 光学定位仪

**Python 依赖：**

```bash
pip install numpy pandas matplotlib scipy scikit-learn pillow openpyxl
pip install ur-rtde
```

部分脚本依赖本地扩展 `AimPosition.pyd`，需在项目根目录下运行，或将根目录加入 `PYTHONPATH`。

## 快速开始 / Quick Start

### 1. 启动 UR5e 并移动到初始位置

```bash
python Init.py
```

确认脚本中的 `ROBOT_IP` 与你的 UR5e 控制器 IP 一致。

### 2. Aimooe 光学定位仪功能演示

```bash
python Demo.py
```

### 3. 工具信息采集

```bash
python Aimooe_timo.py      # PTM-99 专用
python CollectedToolData.py # 完整版
```

### 4. 手眼标定

```bash
cd "hand–eye calibration"
python 手眼标定最终.py
```

### 5. 力控穿刺实验

```bash
cd force
python 导纳控制.py
```

### 6. 力控结果分析绘图

```bash
python force/common_depth_window_force_plot_portable.py
```

## 算法说明 / Algorithms

### 手眼标定

- 基于光学定位仪获取的标记点坐标与机器人 TCP 位姿
- 求解 AX=XB 手眼标定矩阵
- 包含鲁棒优化：MAD 离群剔除、迭代重加权、多阈值过滤
- 精度验证：逐点误差分析、3D 点云重合度、统计分布

### 力控策略

| 算法 | 文件 | 特点 |
|------|------|------|
| 导纳控制 | `导纳控制.py` | 两态状态机、TCP 坐标系、位置漂移补偿 |
| 阻抗控制 | `阻抗控制250hz.py` | 高频阻抗、姿态锁定 |
| 混合力控 | `混合力控带角度穿刺*.py` | 力/位置混合控制、角度穿刺 |
| MPC | `阻抗mpc算法.py` | 模型预测控制、约束优化 |
| 阻抗-导纳融合 | `阻抗导纳融合力控.py` | 两者优势结合 |

### PBVS 视觉伺服

- 基于位置的视觉伺服（Position-Based Visual Servoing）
- 结合光学定位仪实时反馈
- 多目标点跟踪与伺服控制

## 安全说明 / Safety

运行机器人控制脚本前请注意：

- 确认 UR5e IP 地址正确 (`ROBOT_IP`)
- 确保机器人工作空间安全无阻碍
- 随时可触控急停开关
- 新脚本先用低速/低加速度测试
- 力控脚本首次运行建议空载测试

## 数据与结果 / Data & Results

仓库包含完整的实验数据以保障可复现性：

- **标定结果**：变换矩阵 (NPZ/TXT)、验证报告、误差分析表格
- **力控日志**：各实验的 CSV 日志（力、位姿、时间戳）
- **分析图表**：对比图、热力图、误差分布图 (PNG/PDF)

## 注意事项 / Notes

- 部分文件/目录名为中文，建议使用 UTF-8 编码的终端和编辑器
- 部分注释显示为乱码时，切换终端编码至 UTF-8 即可
- `AimPosition.pyd` 是 32 位 Windows 扩展，Python 版本需匹配
- 手眼标定和力控脚本包含实验特定路径，运行前请检查调整

## License

This project is for research and educational purposes.
