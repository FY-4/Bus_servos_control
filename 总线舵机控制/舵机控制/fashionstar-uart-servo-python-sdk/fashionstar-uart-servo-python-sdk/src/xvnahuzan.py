
# 添加uservo.py的系统路径
import sys
sys.path.append("../../src")
# 导入依赖
import time
import struct
import serial
from uservo import UartServoManager

# 参数配置
# 角度定义
SERVO_PORT_NAME =  'COM14'		# 舵机串口号 请根据实际串口进行修改
SERVO_BAUDRATE = 115200			# 舵机的波特率 请根据实际波特率进行修改
SERVO_ID = 8       #舵机ID

# 初始化串口
uart = serial.Serial(port=SERVO_PORT_NAME, baudrate=SERVO_BAUDRATE,\
					 parity=serial.PARITY_NONE, stopbits=1,\
					 bytesize=8,timeout=0)
# 初始化舵机管理器
uservo = UartServoManager(uart, is_debug=True)
time.sleep(0.02)

angle1=0
uservo.set_servo_angle( 8, angle = angle1, interval=0, power=10000)
while True:
    angle1+=45
    time.sleep(1)
    print(f"{angle1} degrees")
    if angle1>=180:
        angle1-=360


    uservo.set_servo_angle(8, angle=angle1, interval=0, velocity=300.0)


