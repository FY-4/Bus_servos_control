import pylx16a
import time

# 初始化控制器并连接舵机
try:
    controller = pylx16a.Controller(port="/dev/ttyUSB0")  # Linux 端口
    # controller = Controller("COM3")  # Windows 端口
    servo_id = 1  # 舵机 ID（需与硬件设置一致）
    servo = controller.get_servo(servo_id)

    # 设置舵机角度（0~240 度）
    servo.set_position(120)  # 转到 120 度
    time.sleep(1)
    servo.set_position(60)   # 转到 60 度
    time.sleep(1)
    servo.set_position(0)  # 转到 60 度

except Exception as e:
    print("Error:", e)