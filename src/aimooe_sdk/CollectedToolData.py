# -*- coding: utf-8 -*-
"""
tool_info_fetcher.py
提取自 demo1.py 的 value=60 功能：获取某路径下的定位工具文件，并获取工具的信息。
独立文件，便于解耦和复用。
优化为高频率实时数据保存到 datamake 文件夹下的 CSV 文件，列名使用中文描述，与控制台输出一致，便于读取。
"""

try:
    from .runtime_path import aimooe_output_dir, aimtools_path, configure_runtime_path, require_aimtools, require_python39
except ImportError:
    from runtime_path import aimooe_output_dir, aimtools_path, configure_runtime_path, require_aimtools, require_python39

configure_runtime_path()
require_python39()

import AimPosition as ap
import time
import pandas as pd
import os
from datetime import datetime


def fetch_tool_info(aimHandle, interfaceType, markerinfo, hardware, toolPath):
    """
    获取工具文件路径下的工具信息，实时保存到 CSV，列名使用中文描述，便于读取。
    :param aimHandle: AimPosition API 句柄
    :param interfaceType: 接口类型（如 ap.E_Interface.I_USB）
    :param markerinfo: 标记点信息对象
    :param hardware: 硬件状态信息对象
    :param toolPath: 工具文件路径
    """
    # 创建 datamake 文件夹
    output_dir = aimooe_output_dir()

    # 初始化 CSV 文件路径，使用时间戳命名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(output_dir, f"tool_info_{timestamp}.csv")

    # 定义 CSV 列名，使用中文描述，与控制台输出一致
    columns = [
        "时间戳", "工具名称", "平均误差", "RMS误差",
        "工具原点_X", "工具原点_Y", "工具原点_Z",
        "工具角度_X", "工具角度_Y", "工具角度_Z",
        "旋转矩阵_Rto_00", "旋转矩阵_Rto_01", "旋转矩阵_Rto_02",
        "旋转矩阵_Rto_10", "旋转矩阵_Rto_11", "旋转矩阵_Rto_12",
        "旋转矩阵_Rto_20", "旋转矩阵_Rto_21", "旋转矩阵_Rto_22",
        "平移矩阵_Tto_X", "平移矩阵_Tto_Y", "平移矩阵_Tto_Z",
        "尖端坐标_X", "尖端坐标_Y", "尖端坐标_Z",
        "尖端方向上另一点坐标_X", "尖端方向上另一点坐标_Y", "尖端方向上另一点坐标_Z",
        "工具坐标系尖端坐标_X", "工具坐标系尖端坐标_Y", "工具坐标系尖端坐标_Z",
        "工具坐标系尖端方向上另一点坐标_X", "工具坐标系尖端方向上另一点坐标_Y", "工具坐标系尖端方向上另一点坐标_Z",
        "标记点坐标"
    ]

    # 创建空的 DataFrame，用于初始化 CSV 文件
    if not os.path.exists(csv_path):
        pd.DataFrame(columns=columns).to_csv(csv_path, index=False, encoding='utf-8-sig')

    r = ap.Aim_SetToolInfoFilePath(aimHandle, toolPath)
    print("工具路径：", ap.Aim_GetToolInfoFilePath(aimHandle))

    toolSize = ap.Aim_GetCountOfToolInfo(aimHandle)
    print("工具数量：", toolSize)

    if toolSize != 0:
        res = ap.Aim_GetAllToolFilesBaseInfo(aimHandle, toolSize)
        if len(res) != 0:
            for i in range(toolSize):
                print("工具名字：", res[i]['name'])
        else:
            print("当前目录没有工具，请检查工具路径")

    try:
        while True:
            r = ap.Aim_GetMarkerAndStatusFromHardware(aimHandle, interfaceType, markerinfo, hardware)
            while r == ap.E_ReturnValue.AIMOOE_NOT_REFLASH:
                time.sleep(0.01)
                r = ap.Aim_GetMarkerAndStatusFromHardware(aimHandle, interfaceType, markerinfo, hardware)
                if r != ap.E_ReturnValue.AIMOOE_OK:
                    break
            if r != ap.E_ReturnValue.AIMOOE_OK:
                break

            residualIndex = list(range(markerinfo.MarkerNumber))
            mtoolsrlt = ap.T_AimToolDataResult()
            r = ap.Aim_FindToolInfo(aimHandle, markerinfo, mtoolsrlt, 0)
            if r == ap.E_ReturnValue.AIMOOE_OK:
                prlt = mtoolsrlt
                while prlt:
                    if prlt.validflag:
                        PI = 3.1415962
                        # 获取当前时间戳
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                        # 收集工具信息
                        tool_data = {
                            "时间戳": current_time,
                            "工具名称": prlt.toolname,
                            "平均误差": prlt.MeanError,
                            "RMS误差": prlt.Rms,
                            "工具原点_X": prlt.OriginCoor[0],
                            "工具原点_Y": prlt.OriginCoor[1],
                            "工具原点_Z": prlt.OriginCoor[2],
                            "工具角度_X": prlt.rotationvector[0] * 180 / PI,
                            "工具角度_Y": prlt.rotationvector[1] * 180 / PI,
                            "工具角度_Z": prlt.rotationvector[2] * 180 / PI,
                            "旋转矩阵_Rto_00": prlt.Rto[0][0],
                            "旋转矩阵_Rto_01": prlt.Rto[0][1],
                            "旋转矩阵_Rto_02": prlt.Rto[0][2],
                            "旋转矩阵_Rto_10": prlt.Rto[1][0],
                            "旋转矩阵_Rto_11": prlt.Rto[1][1],
                            "旋转矩阵_Rto_12": prlt.Rto[1][2],
                            "旋转矩阵_Rto_20": prlt.Rto[2][0],
                            "旋转矩阵_Rto_21": prlt.Rto[2][1],
                            "旋转矩阵_Rto_22": prlt.Rto[2][2],
                            "平移矩阵_Tto_X": prlt.Tto[0],
                            "平移矩阵_Tto_Y": prlt.Tto[1],
                            "平移矩阵_Tto_Z": prlt.Tto[2],
                            "尖端坐标_X": prlt.tooltip[0],
                            "尖端坐标_Y": prlt.tooltip[1],
                            "尖端坐标_Z": prlt.tooltip[2],
                            "尖端方向上另一点坐标_X": prlt.toolmid[0],
                            "尖端方向上另一点坐标_Y": prlt.toolmid[1],
                            "尖端方向上另一点坐标_Z": prlt.toolmid[2],
                            "工具坐标系尖端坐标_X": prlt.toolCstip[0],
                            "工具坐标系尖端坐标_Y": prlt.toolCstip[1],
                            "工具坐标系尖端坐标_Z": prlt.toolCstip[2],
                            "工具坐标系尖端方向上另一点坐标_X": prlt.toolCsmid[0],
                            "工具坐标系尖端方向上另一点坐标_Y": prlt.toolCsmid[1],
                            "工具坐标系尖端方向上另一点坐标_Z": prlt.toolCsmid[2],
                            "标记点坐标": ""
                        }

                        # 收集标记点坐标
                        marker_coords = []
                        for idx in prlt.toolptidx:
                            if idx in residualIndex:
                                residualIndex.remove(idx)
                            if idx < 0:
                                marker_coords.append("0 0 0")
                            else:
                                coord = f"{markerinfo.MarkerCoordinate[idx * 3 + 0]} {markerinfo.MarkerCoordinate[idx * 3 + 1]} {markerinfo.MarkerCoordinate[idx * 3 + 2]}"
                                marker_coords.append(coord)
                        tool_data["标记点坐标"] = ";".join(marker_coords)

                        # 打印工具信息
                        print(f"找到工具: {prlt.toolname}  平均误差{prlt.MeanError} RMS误差{prlt.Rms}")
                        print(f"工具原点: {prlt.OriginCoor[0]}, {prlt.OriginCoor[1]}, {prlt.OriginCoor[2]}")
                        print(
                            f"工具角度: {prlt.rotationvector[0] * 180 / PI}, {prlt.rotationvector[1] * 180 / PI}, {prlt.rotationvector[2] * 180 / PI}")
                        print("旋转矩阵 Rto:")
                        for row in prlt.Rto:
                            print(f"  {row[0]}, {row[1]}, {row[2]}")
                        print(f"平移矩阵 Tto: {prlt.Tto[0]}, {prlt.Tto[1]}, {prlt.Tto[2]}")
                        print("标记点坐标:")
                        print(
                            f"工具在系统坐标系下原点坐标 (OriginCoor): {prlt.OriginCoor[0]}, {prlt.OriginCoor[1]}, {prlt.OriginCoor[2]}")
                        print(f"工具在系统坐标系下尖端坐标 (tooltip): {prlt.tooltip[0]}, {prlt.tooltip[1]}, {prlt.tooltip[2]}")
                        print(f"工具在系统坐标系下尖端方向上另一点坐标 (toolmid): {prlt.toolmid[0]}, {prlt.toolmid[1]}, {prlt.toolmid[2]}")
                        print(f"工具坐标系尖端坐标 (toolCstip): {prlt.toolCstip[0]}, {prlt.toolCstip[1]}, {prlt.toolCstip[2]}")
                        print(
                            f"工具坐标系尖端方向上另一点坐标 (toolCsmid): {prlt.toolCsmid[0]}, {prlt.toolCsmid[1]}, {prlt.toolCsmid[2]}")
                        for coord in marker_coords:
                            print(coord)

                        # 收集并打印离散点（仅打印，不保存到 CSV）
                        if len(residualIndex) > 0:
                            print(f"共{len(residualIndex)}个离散点：")
                            for i, j in enumerate(residualIndex):
                                coord = f"{markerinfo.MarkerCoordinate[j * 3 + 0]}, {markerinfo.MarkerCoordinate[j * 3 + 1]}, {markerinfo.MarkerCoordinate[j * 3 + 2]}"
                                print(f"{i}: {coord}")

                        # 实时保存到 CSV
                        try:
                            df = pd.DataFrame([tool_data], columns=columns)
                            df.to_csv(csv_path, mode='a', header=not os.path.getsize(csv_path), index=False,
                                      encoding='utf-8-sig')
                            print(f"数据已追加到: {csv_path}")
                        except Exception as e:
                            print(f"写入 CSV 失败: {e}")

                    pnext = prlt.next
                    del prlt
                    prlt = pnext
            else:
                del mtoolsrlt
                break
    except KeyboardInterrupt:
        print("用户中断程序，保存已收集的数据")
    except Exception as e:
        print(f"程序异常: {e}")
    finally:
        print("查找结束")


if __name__ == "__main__":
    require_aimtools()
    # 初始化 AimPosition API
    aimHandle = ap.Aim_API_Initial()
    toolPath = aimtools_path()
    if aimHandle is not None:
        interfaceType = ap.E_Interface.I_USB
        pospara = ap.T_AIMPOS_DATAPARA()
        result = ap.Aim_ConnectDevice(aimHandle, interfaceType, pospara)
        if result == ap.E_ReturnValue.AIMOOE_OK:
            markerinfo = ap.T_MarkerInfo()
            hardware = ap.T_AimPosStatusInfo()
            ap.Aim_SetAcquireData(aimHandle, interfaceType, ap.E_DataType.DT_NONE)
            ap.Aim_GetMarkerAndStatusFromHardware(aimHandle, interfaceType, markerinfo, hardware)
            # 调用函数
            fetch_tool_info(aimHandle, interfaceType, markerinfo, hardware, toolPath)
        else:
            print("连接定位失败")
    else:
        print("初始化失败，请重启定位仪")
