# -*- coding: utf-8 -*-
"""
tool_info_fetcher.py
提取自 demo1.py 的 value=60 功能：获取某路径下的定位工具文件，并获取工具的信息。
独立文件，便于解耦和复用。
优化为高频率实时数据保存到 datamake 文件夹下的 CSV 文件，列名使用中文描述，与控制台输出一致，便于读取。
【本版本修改】：仅输出与保存 PTM-99（体膜工具）对 PBVS 有用的信息（OriginCoor + Rto + 标记点坐标）
"""

import AimPosition as ap
import time
import pandas as pd
import os
from datetime import datetime


def fetch_tool_info(aimHandle, interfaceType, markerinfo, hardware, toolPath):
    """
    获取工具文件路径下的工具信息，实时保存到 CSV，列名使用中文描述，便于读取。
    仅输出 PTM-99 相关数据。
    :param aimHandle: AimPosition API 句柄
    :param interfaceType: 接口类型（如 ap.E_Interface.I_USB）
    :param markerinfo: 标记点信息对象
    :param hardware: 硬件状态信息对象
    :param toolPath: 工具文件路径
    """
    # 创建 datamake 文件夹
    output_dir = "datatimo"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 初始化 CSV 文件路径，使用时间戳命名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(output_dir, f"tool_info_PTM99_{timestamp}.csv")

    # ✅ 仅保留 PBVS 必要字段：OriginCoor + Rto + 标记点坐标
    columns = [
        "时间戳", "工具名称",
        "工具原点_X", "工具原点_Y", "工具原点_Z",
        "旋转矩阵_Rto_00", "旋转矩阵_Rto_01", "旋转矩阵_Rto_02",
        "旋转矩阵_Rto_10", "旋转矩阵_Rto_11", "旋转矩阵_Rto_12",
        "旋转矩阵_Rto_20", "旋转矩阵_Rto_21", "旋转矩阵_Rto_22",
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

                    # ✅ 只处理 PTM-99，不是 PTM-99 直接跳过：不打印、不保存
                    if prlt.toolname != "PTM-99":
                        pnext = prlt.next
                        del prlt
                        prlt = pnext
                        continue

                    if prlt.validflag:
                        # 获取当前时间戳
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

                        # ✅ 只收集 PBVS 必要信息
                        tool_data = {
                            "时间戳": current_time,
                            "工具名称": prlt.toolname,
                            "工具原点_X": prlt.OriginCoor[0],
                            "工具原点_Y": prlt.OriginCoor[1],
                            "工具原点_Z": prlt.OriginCoor[2],
                            "旋转矩阵_Rto_00": prlt.Rto[0][0],
                            "旋转矩阵_Rto_01": prlt.Rto[0][1],
                            "旋转矩阵_Rto_02": prlt.Rto[0][2],
                            "旋转矩阵_Rto_10": prlt.Rto[1][0],
                            "旋转矩阵_Rto_11": prlt.Rto[1][1],
                            "旋转矩阵_Rto_12": prlt.Rto[1][2],
                            "旋转矩阵_Rto_20": prlt.Rto[2][0],
                            "旋转矩阵_Rto_21": prlt.Rto[2][1],
                            "旋转矩阵_Rto_22": prlt.Rto[2][2],
                            "标记点坐标": ""
                        }

                        # 收集标记点坐标（保留你原逻辑）
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

                        # ✅ 终端实时输出（保持你原来那种“详细逐项打印”的风格，但只输出必要字段）
                        print(f"找到工具: {prlt.toolname}")
                        print(f"工具原点(OriginCoor): {prlt.OriginCoor[0]}, {prlt.OriginCoor[1]}, {prlt.OriginCoor[2]}")
                        print("旋转矩阵 Rto:")
                        for row in prlt.Rto:
                            print(f"  {row[0]}, {row[1]}, {row[2]}")
                        print("标记点坐标:")
                        for coord in marker_coords:
                            print(coord)

                        # 你原来有“离散点”输出，这里也保留（对调试丢点很有帮助）
                        if len(residualIndex) > 0:
                            print(f"共{len(residualIndex)}个离散点：")
                            for i, j in enumerate(residualIndex):
                                coord = f"{markerinfo.MarkerCoordinate[j * 3 + 0]}, {markerinfo.MarkerCoordinate[j * 3 + 1]}, {markerinfo.MarkerCoordinate[j * 3 + 2]}"
                                print(f"{i}: {coord}")

                        # ✅ 实时保存到 CSV（只写 PTM-99，且只写必要列）
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
    # 初始化 AimPosition API
    aimHandle = ap.Aim_API_Initial()
    toolPath = './AimTools/'
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
