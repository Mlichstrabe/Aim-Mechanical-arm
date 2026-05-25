# aimooe_ur5e 30 天离线学习执行表

适用情况：Aimooe 定位仪和 UR5e 暂时不在身边，但你希望每天能按步骤推进。建议每天 2-3 小时。如果当天时间不够，优先完成“今日必须产出”。

## 每天固定流程

1. 用 10 分钟回顾昨天的笔记，写下今天要解决的 1 个核心问题。
2. 用 60-90 分钟读代码或文档，只围绕当天主题，不发散。
3. 用 40-60 分钟做离线练习，能运行就运行，不能运行就画数据流或手算。
4. 用 15 分钟写当天总结：今天学会了什么、还有什么不懂、明天先看哪里。

建议新建一个自己的笔记文件，例如 `notes/daily_learning.md`。如果暂时不想改仓库，也可以写在本地 Obsidian、Notion 或普通 Markdown 里。

## 第 1 周：先摸清项目，不急着学 ROS

### Day 1：建立项目地图

目标：知道这个项目大概由哪几块组成。

执行：

1. 阅读 `README.md` 的 Overview、Layout、Quick Start。
2. 打开这些文件，只看开头注释和主函数：`src/aimooe_sdk/Demo.py`、`src/aimooe_sdk/demo1.py`、`src/aimooe_sdk/Aimooe_timo.py`、`src/aimooe_sdk/CollectedToolData.py`、`src/ur5e_control/Init.py`。
3. 画一张项目结构图，至少包含：Aimooe 定位仪、UR5e、坐标变换、手眼标定、needle_tracking 整合。
4. 运行：

```powershell
python run_offline_demo.py
```

今日必须产出：

- 一张“项目模块图”。
- 一句话解释：这个项目不是单纯 ROS 项目，而是“定位仪 + 坐标变换 + UR5e 执行”的实验链路。

### Day 2：读懂 Aimooe demo 菜单

目标：知道 `src/aimooe_sdk/Demo.py` / `src/aimooe_sdk/demo1.py` 里每个 case 大概做什么。

执行：

1. 阅读 `src/aimooe_sdk/Demo.py` 的 `caseTitle()`。
2. 搜索并阅读 `whichcase(value, ...)`。
3. 重点标记 case 60 和 case 62。
4. 写一个表格：case 编号、功能、是否和本项目主线有关。

今日必须产出：

- 能说清 case 60 偏向 tool 信息读取，case 62 偏向空间配准。

### Day 3：理解 marker 点

目标：区分 marker 点和 tool。

执行：

1. 阅读 `src/aimooe_sdk/Demo.py` 中调用 `Aim_GetMarkerAndStatusFromHardware` 的代码。
2. 找到 `MarkerNumber`、`MarkerCoordinate`、`PhantomMarkerGroupNumber`。
3. 阅读 `docs/AIMOOE_OUTPUT_FIELDS.md` 中 marker 相关字段。
4. 用自己的话写出：一个 marker 点是什么，为什么会丢点，为什么会有幻影点。

今日必须产出：

- 一段 150 字以内解释：marker 是定位仪直接看到的点，tool 是由多个 marker 匹配出来的刚体工具。

### Day 4：理解 tool 识别

目标：知道 Aimooe 怎么从 marker 变成工具位姿。

执行：

1. 阅读 `src/aimooe_sdk/Aimooe_timo.py` 中 `fetch_tool_info()`。
2. 找到 `Aim_SetToolInfoFilePath`、`Aim_GetCountOfToolInfo`、`Aim_FindToolInfo`。
3. 对照 `data/sample/tool_pose_frame.json`。
4. 写出 `toolname`、`validflag`、`MeanError`、`Rms` 的作用。

今日必须产出：

- 一张“marker -> tool -> pose”的流程图。

### Day 5：理解工具位姿字段

目标：知道 `OriginCoor`、`Rto`、`tooltip` 怎么用。

执行：

1. 阅读 `src/aimooe_sdk/CollectedToolData.py` 中保存 CSV 的字段。
2. 对照 `docs/AIMOOE_OUTPUT_FIELDS.md`。
3. 在 `data/sample/tool_pose_frame.json` 里手动改 `OriginCoor` 的一个值，再运行：

```powershell
python run_offline_demo.py
```

注意：当前 demo 只是展示 tool frame，不把 tool pose 用进 robot 目标，所以 robot 目标不会因为改 `OriginCoor` 而变化。这是正常的。

今日必须产出：

- 写清楚：`OriginCoor` 是工具原点，`tooltip` 是工具尖端，穿刺任务里通常更关心尖端。

### Day 6：整理 Aimooe 学习笔记

目标：把前 5 天内容压缩成你自己的速查表。

执行：

1. 写一页 Aimooe 速查笔记。
2. 必须包含：连接设备、读 marker、读 tool、判断 tool 是否有效、保存 CSV。
3. 把你还不懂的 SDK 函数列出来。

今日必须产出：

- 一份“我看 Aimooe 代码时先找哪些函数”的清单。

### Day 7：第 1 周复盘

目标：确认你已经能读定位仪相关代码。

自测问题：

1. marker 和 tool 有什么区别？
2. `.aimtool` 文件大概起什么作用？
3. `validflag` 为 false 时能不能控制机械臂？
4. `OriginCoor` 和 `tooltip` 哪个更接近穿刺针尖？
5. case 62 为什么重要？

今日必须产出：

- 如果 5 个问题能回答 4 个，进入第 2 周。
- 如果不行，回到 Day 3-Day 5 重新读。

## 第 2 周：坐标系、矩阵和空间配准

### Day 8：坐标系入门

目标：建立“任何点都属于某个坐标系”的意识。

执行：

1. 阅读 `docs/INTEGRATION_NEEDLE_TRACKING.md` 的坐标变换链。
2. 写出这三个坐标系的含义：`ct_scene_mm`、`optical_mm`、`robot_base_mm`。
3. 打开 `data/sample/calibration_chain.json`，标出每个 transform 的 `from` 和 `to`。

今日必须产出：

- 一张 `CT -> optical -> robot` 的箭头图。

### Day 9：手算一次 `R @ p + t`

目标：不靠代码也能算一个 3D 点变换。

执行：

1. 打开 `tests/test_offline_bridge.py`。
2. 找到 `test_apply_transform_rotates_and_translates_point`。
3. 手算 `[1, 2, 3]` 经过旋转和平移后为什么是 `[8, 21, 33]`。
4. 运行：

```powershell
python -m unittest tests.test_offline_bridge
```

今日必须产出：

- 一页手算过程。

### Day 10：读 `src/offline_bridge/transforms.py`

目标：理解离线坐标转换代码。

执行：

1. 阅读 `validate_transform()`，理解为什么要检查 3x3 和 3D 点。
2. 阅读 `apply_transform()`，逐行对应 Day 9 的手算。
3. 阅读 `compose_transform()`，理解为什么是“先 second，再 first”。
4. 给每个函数写一句中文解释。

今日必须产出：

- 能说清 `compose_transform(optical_to_robot, ct_to_optical)` 得到的是 `ct_to_robot`。

### Day 11：理解方向写反的风险

目标：知道坐标变换最危险的 bug 是方向错。

执行：

1. 在纸上写：`ct_to_optical` 和 `optical_to_ct` 不是一回事。
2. 临时把测试里的 transform 顺序调反，观察报错或结果变化。看完后改回去。
3. 写一个错误案例：如果把 robot 点当 optical 点，会发生什么。

今日必须产出：

- 一段结论：矩阵数字本身不够，必须带 `from` / `to`。

### Day 12：理解空间配准 case 62

目标：知道 case 62 在项目里对应哪一步。

执行：

1. 阅读 `src/aimooe_sdk/Demo.py` 里 `elif value == 62:`。
2. 找到 `CTMarkerPoint`。
3. 找到 `Aim_InitMappingPointSetsForMarkerSpaceReg` 和 `Aim_MappingPointSetsForMarkerSpaceReg`。
4. 对照 `docs/INTEGRATION_NEEDLE_TRACKING.md`，理解它为什么产生 `CT -> optical`。

今日必须产出：

- 一句话解释：case 62 用 CT 中的 fiducial 点和定位仪看到的点建立空间配准。

### Day 13：理解手眼标定的位置

目标：知道手眼标定不是空间配准，但两者会串起来。

执行：

1. 复读 `docs/INTEGRATION_NEEDLE_TRACKING.md` 的 L1/L2/L3。
2. 写清：L1 针尖注册、L2 手眼、L3 CT 到光学空间配准分别解决什么问题。
3. 搜索 README 里 “AX=XB”。

今日必须产出：

- 一张 L1/L2/L3 表格：输入、输出、用途。

### Day 14：第 2 周复盘

目标：确认坐标链路能讲清。

自测问题：

1. `p_opt = R_ct2opt @ p_ct + t_ct2opt` 是什么意思？
2. `p_robot = R_opt2rob @ p_opt + t_opt2rob` 是什么意思？
3. 为什么不应该只保存一个裸矩阵？
4. case 62 和手眼标定有什么区别？
5. mm 和 m 混用会导致什么问题？

今日必须产出：

- 能不用看文档画出 `CT -> optical -> robot`。

## 第 3 周：UR5e、RTDE、mock robot

### Day 15：读 `src/ur5e_control/Init.py`

目标：读懂最小 UR5e 控制脚本。

执行：

1. 阅读 `src/ur5e_control/Init.py`。
2. 标出 `ROBOT_IP`、`START_POINT_DEGREES`、`START_POINT_RADIANS`。
3. 理解 `rtde_control` 和 `rtde_receive` 的区别。
4. 写出 `moveJ` 的输入是什么。

今日必须产出：

- 一句话解释：`moveJ` 是关节角目标，不是笛卡尔位置目标。

### Day 16：理解安全参数

目标：知道速度和加速度为什么是安全问题。

执行：

1. 阅读 README 的 Safety。
2. 查 `src/ur5e_control/Init.py` 里的默认 `velocity=1.05`、`acceleration=1.4`。
3. 写一份设备到手前检查清单：IP、急停、空间、速度、旁站人员。

今日必须产出：

- 一份“第一次接 UR5e 不做什么”的清单。

### Day 17：理解 mock robot

目标：知道为什么没有设备也能练执行链路。

执行：

1. 阅读 `src/offline_bridge/mock_robot.py`。
2. 阅读 `tests/test_offline_bridge.py` 里的 `MockRobotTests`。
3. 运行：

```powershell
python run_offline_demo.py
```

4. 解释输出里的 `hardware_connected: False`。

今日必须产出：

- 一句话解释：mock robot 不是控制机械臂，而是提前检查目标点、单位和命令格式。

### Day 18：RTDE 和 socket 的分工

目标：建立通信协议层面的基本认识。

执行：

1. 在笔记里写两个标题：RTDE、socket。
2. RTDE 下写：实时状态、控制接口、UR 官方生态常用。
3. socket 下写：自定义通信、脚本交互、数据转发。
4. 回到师兄聊天记录，把“机械臂就是 RTDE socket”翻译成你能理解的话。

今日必须产出：

- 一段解释：本项目先用 RTDE 理解控制，socket 作为后续补充。

### Day 19：从目标点到运动命令

目标：理解 `entry_robot_mm` 到 robot command 的路径。

执行：

1. 打开 `run_offline_demo.py`。
2. 找到 `transform_plan_ct_to_robot()`。
3. 找到 `robot.move_l(transformed_plan["entry"], ...)`。
4. 修改 `data/sample/puncture_plan.json` 的 `entry`，观察输出。

今日必须产出：

- 写出：输入改了哪里，输出改了哪里，为什么。

### Day 20：单位检查日

目标：专门防止 mm/m 错误。

执行：

1. 在笔记中写：Aimooe/CT 侧默认 mm，UR RTDE TCP pose 常见是 m/rad。
2. 检查 `src/offline_bridge/mock_robot.py` 中字段名为什么叫 `target_mm`。
3. 写一个假设：如果把 500 mm 当 500 m 发给机器人会怎样。

今日必须产出：

- 一条规则：真实控制前必须显式做 mm -> m 转换，不能隐式猜。

### Day 21：第 3 周复盘

目标：确认你能解释“离线执行”。

自测问题：

1. `moveJ` 和 `moveL` 有什么区别？
2. 为什么没有设备时不应该 import 真实 RTDE 接口来乱试？
3. mock robot 帮你提前发现哪类问题？
4. 真实 UR5e 运行前最重要的 3 个安全检查是什么？
5. `target_mm` 最终发给真实 robot 前可能要做什么单位转换？

今日必须产出：

- 一份“设备到手第一天验证顺序”。

## 第 4 周：整合、ROS2 预备、交接输出

### Day 22：整理最小闭环

目标：把离线链路完整串起来。

执行：

1. 画出：

```text
puncture_plan.json -> calibration_chain.json -> transforms.py -> mock_robot.py
```

2. 给每条箭头写输入/输出。
3. 运行测试：

```powershell
python -m unittest discover -s tests
```

今日必须产出：

- 一张最小闭环数据流图。

### Day 23：读 needle_tracking 整合文档

目标：知道外部项目和本项目怎么接。

执行：

1. 阅读 `docs/INTEGRATION_NEEDLE_TRACKING.md`。
2. 标记 `puncture_plan.json`、`space_reg.npz`、`execute_ct_puncture.py`。
3. 写清：needle_tracking 负责什么，aimooe_ur5e 负责什么。

今日必须产出：

- 一张两项目分工表。

### Day 24：设计未来真实桥接脚本

目标：不写真实硬件控制，也能设计接口。

执行：

1. 在笔记里设计 `coord_bridge.py` 应该做什么。
2. 输入：plan、ct_to_optical、optical_to_robot。
3. 输出：robot frame 下的 entry/target。
4. 写出 3 个必须检查的错误：缺字段、坐标系不匹配、单位不明确。

今日必须产出：

- 一个未来脚本接口草图。

### Day 25：ROS2 只学必要概念

目标：知道 ROS2 将来放在哪，不急着实现。

执行：

1. 只学 5 个词：node、topic、service、tf2、launch。
2. 把离线链路映射成 ROS2：
   - 定位仪数据：topic
   - 目标点转换：service 或 node 内部函数
   - 坐标树：tf2
   - 启动多个节点：launch
3. 写出为什么现在先不做 ROS2。

今日必须产出：

- 一张“Python 离线模块 -> ROS2 概念”的对应表。

### Day 26：代码质量和交接笔记

目标：让别人也能看懂你的接手过程。

执行：

1. 检查 `docs/OFFLINE_ONBOARDING.md`、`docs/OFFLINE_DEMO.md`、`docs/AIMOOE_OUTPUT_FIELDS.md`。
2. 把你自己的疑问追加到笔记，不要塞进 README。
3. 运行：

```powershell
python -m unittest discover -s tests
python run_offline_demo.py
```

今日必须产出：

- 一份“我还需要问师兄的问题”。

### Day 27：准备问师兄的问题

目标：把问题问具体，避免泛泛问“这个项目怎么跑”。

建议问题：

1. `Aim-Mechanical-arm` 目录是否漏传源码？
2. 当前真实使用的 `.aimtool` 文件是哪几个？
3. `ROBOT_IP`、UR5e 网络配置和安全限速是多少？
4. L2 手眼标定应保存到哪个文件？（`data/calibration/HandEye_Calibration_Matrix.npz`）
5. case 62 里那组 CT 点是否只是示例，还是某次实验真实点？
6. 设备到手后推荐先跑哪个脚本，只读数据还是直接移动？

今日必须产出：

- 一条可以直接发给师兄的清晰问题列表。

### Day 28：模拟一次完整讲解

目标：像组会汇报一样讲清项目。

执行：

1. 用 5 分钟讲项目目标。
2. 用 5 分钟讲 Aimooe 数据。
3. 用 5 分钟讲坐标链。
4. 用 5 分钟讲 UR5e 执行。
5. 用 5 分钟讲你现在能离线跑什么、还缺什么设备验证。

今日必须产出：

- 一份 1 页汇报提纲。

### Day 29：设备到手前最终检查

目标：把离线阶段收口。

执行：

1. 运行全部离线验证。
2. 检查你是否能回答前 3 周所有自测题。
3. 写一份“设备到手第一天只做这些”的操作单。

今日必须产出：

- 一份低速验证 checklist。

### Day 30：月度复盘和下一阶段计划

目标：决定下一阶段学什么。

执行：

1. 复盘一个月：最清楚的 3 件事、最不清楚的 3 件事。
2. 如果设备还没到：继续补 ROS2/tf2 和 URScript。
3. 如果设备到了：按 Day 29 checklist 做只读验证和低速验证。
4. 如果要进入研究：再看 PBVS、力控、手眼标定精度分析。

今日必须产出：

- 下一阶段 2 周计划：设备验证版或继续离线版。

## 每周交付物汇总

| 周 | 交付物 | 判断标准 |
| --- | --- | --- |
| 第 1 周 | Aimooe 字段和 tool 识别笔记 | 能解释 marker、tool、`OriginCoor`、`tooltip` |
| 第 2 周 | 坐标链路图和手算过程 | 能解释 `CT -> optical -> robot` |
| 第 3 周 | UR5e/mock robot 安全执行笔记 | 能解释 RTDE、`moveJ`、mock robot |
| 第 4 周 | 最小闭环图、问师兄清单、设备验证 checklist | 能讲清项目并准备接设备 |

## 每天不要做的事

- 不要第一周就陷进 ROS2 教程。
- 不要没有设备时强行调真实硬件库。
- 不要把 README 里列出的所有旧实验脚本都当成当前必须掌握。
- 不要跳过坐标系直接看控制代码。
- 不要在没有安全检查时运行真实机器人移动脚本。
