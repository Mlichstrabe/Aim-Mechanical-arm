# Aimooe 输出字段速查

这份表用于读 `src/aimooe_sdk/Demo.py`、`src/aimooe_sdk/demo1.py`、`src/aimooe_sdk/Aimooe_timo.py` 和 `src/aimooe_sdk/CollectedToolData.py`。字段名以现有代码中的命名为准。

| 字段 | 含义 | 离线阶段怎么理解 |
| --- | --- | --- |
| `MarkerNumber` | 当前帧识别到的 marker 点数量 | 点越少，越可能丢点或遮挡 |
| `MarkerCoordinate` | marker 的三维坐标数组 | 通常按 `[x0, y0, z0, x1, y1, z1, ...]` 展开 |
| `toolname` | 被识别出的工具名称 | 例如 `PTM-99`，需要对应 `.aimtool` 文件 |
| `validflag` | 当前工具识别是否有效 | 无效时不要用于控制机械臂 |
| `MeanError` / `Rms` | 工具匹配误差 | 用于判断工具识别质量 |
| `OriginCoor` | 工具原点在定位仪坐标系下的位置 | PBVS 和坐标转换常用的核心位置 |
| `Rto` | 工具坐标系到定位仪坐标系的旋转矩阵 | 描述工具姿态，必须和 `OriginCoor` 配套使用 |
| `Tto` | 工具到定位仪的平移项 | 和 `Rto` 一起描述工具位姿 |
| `tooltip` | 工具尖端在定位仪坐标系下的位置 | 穿刺针/探针类工具尤其重要 |
| `toolmid` | 工具尖端方向上的另一个点 | 可用于估计工具轴线方向 |
| `toolptidx` | 当前工具匹配到的 marker 索引 | 用于从原始 marker 点追溯工具构成 |

## 读代码时的主线

1. `Aim_GetMarkerAndStatusFromHardware` 读取当前帧 marker。
2. `Aim_FindToolInfo` 根据 `.aimtool` 文件把 marker 匹配为工具。
3. 代码从 `prlt` 读取 `OriginCoor`、`Rto`、`tooltip` 等字段。
4. 后续算法应先检查 `validflag` 和误差，再使用位姿数据。

## 常见坑

- 不要把定位仪坐标系误认为机器人坐标系。
- 不要只保存点坐标而丢掉坐标系名称。
- 不要在工具无效、marker 遮挡或误差明显异常时继续生成机器人运动。
- 不要混用 mm 和 m。现有定位/标定文档默认按 mm 理解，UR RTDE 常见 TCP pose 是 m/rad，需要在真实控制前做单位检查。
