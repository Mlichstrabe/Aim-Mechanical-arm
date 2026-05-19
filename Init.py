import math
import rtde_control
import rtde_receive

ROBOT_IP = "192.168.56.101"  # 机械臂 IP 地址

# 初始位置角度（度）
START_POINT_DEGREES = [0, -90, 90, 0, 90, 0]
# 转换为弧度
START_POINT_RADIANS = [math.radians(a) for a in START_POINT_DEGREES]

def move_to_initial_position(robot_ip=ROBOT_IP, velocity=1.05, acceleration=1.4):
    """
    直接移动机械臂到初始位置，无需中间路径。
    """
    # 初始化 RTDE 控制和接收接口
    rtde_c = rtde_control.RTDEControlInterface(robot_ip)
    rtde_r = rtde_receive.RTDEReceiveInterface(robot_ip)

    try:
        current_joint_angles = rtde_r.getActualQ()
        print("当前关节角度 (弧度):", [round(a, 4) for a in current_joint_angles])

        print("正在移动到初始位置...")
        rtde_c.moveJ(START_POINT_RADIANS, speed=velocity, acceleration=acceleration)
        print("机器人已到达初始位置:", [round(a, 4) for a in START_POINT_RADIANS])

    except Exception as e:
        print("移动过程中发生错误:", e)

    finally:
        rtde_c.disconnect()
        print("RTDE 控制接口已断开连接。")

if __name__ == "__main__":
    move_to_initial_position()
