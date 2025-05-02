import cv2
from ultralytics import YOLO
import serial
from uservo import UartServoManager
import time


SERVO_PORT = 'COM14'
PAN_ID = 8
CAMERA_ID = 1
THRESHOLD = 10
MOVE_SPEED = 10

uart = serial.Serial(SERVO_PORT, baudrate=115200, timeout=0.5)
servo = UartServoManager(uart, is_scan_servo=False)
model = YOLO('yolov11n-face.pt')

try:
    cap = cv2.VideoCapture(CAMERA_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    servo.set_wheel(PAN_ID, servo.WHEEL_MODE_STOP)
    time.sleep(5)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 人脸检测
        results = model.predict(frame, verbose=False, conf=0.7)
        boxes = results[0].boxes.xyxy.cpu().numpy()

        if len(boxes) > 0:
            # 取最大人脸
            x1, y1, x2, y2 = map(int, boxes[0])
            face_cx = (x1 + x2) // 2
            dx = 320 - face_cx

            if dx > THRESHOLD:
                print("向左转")
                servo.set_wheel(PAN_ID, servo.WHEEL_MODE_NORMAL,
                                is_cw=False, mean_dps=MOVE_SPEED)
            elif dx < -THRESHOLD:
                print("向右转")
                servo.set_wheel(PAN_ID, servo.WHEEL_MODE_NORMAL,
                                is_cw=True, mean_dps=MOVE_SPEED)
            else:  # 在中心区域
                print("停止")
                servo.set_wheel(PAN_ID, servo.WHEEL_MODE_STOP)

            # 绘制检测框
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.line(frame, (320, 0), (320, 480), (0, 255, 0), 2)  # 中心线

        cv2.imshow('Face Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"发生错误: {str(e)}")
finally:
    # 清理资源
    cap.release()
    cv2.destroyAllWindows()
    servo.set_wheel(PAN_ID, servo.WHEEL_MODE_STOP)  # 确保停止
    uart.close()