import cv2
import time
from djitellopy import Tello
from cvzone.HandTrackingModule import HandDetector

# 初始化并连接无人机
tello = Tello()
tello.connect()
print(f"电池电量: {tello.get_battery()}%")
tello.streamon()

# 初始化摄像头和手部识别
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = HandDetector(maxHands=1)

# 为检查悬停状态时间初始化变量
hover_start_time = None

# 定义根据手势控制无人机的函数
def control_drone(gesture):
    if gesture == "up":
        tello.move_up(30)
    elif gesture == "down":
        tello.move_down(30)
    elif gesture == "left":
        tello.rotate_counter_clockwise(30)
    elif gesture == "right":
        tello.rotate_clockwise(30)
    elif gesture == "forward":
        tello.move_forward(30)
    elif gesture == "back":
        tello.move_back(30)
    elif gesture == "land":
        tello.land()

# 主循环
while True:
    success, img = cap.read()
    if not success:
        break
    
    # 手部识别
    hands, img = detector.findHands(img)
    
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        # 识别手势并控制无人机
        if fingers == [1, 1, 1, 1, 1]:  # 所有手指张开时向前
            control_drone("forward")
            hover_start_time = None  # 当执行非悬停动作时重置
        elif fingers == [0, 0, 0, 0, 0]:  # 所有手指收拢时向后
            control_drone("back")
            hover_start_time = None
        elif fingers == [0, 1, 0, 0, 0]:  # 仅食指张开时向上
            control_drone("up")
            hover_start_time = None
        elif fingers == [0, 1, 1, 0, 0]:  # 食指和中指张开时向下
            control_drone("down")
            hover_start_time = None
        elif fingers == [1, 0, 0, 0, 0]:  # 仅拇指张开时向左
            control_drone("left")
            hover_start_time = None
        elif fingers == [0, 0, 0, 0, 1]:  # 仅小指张开时向右
            control_drone("right")
            hover_start_time = None
    else:
        # 未识别到手时悬停
        if hover_start_time is None:
            hover_start_time = time.time()  # 记录悬停开始时间
        else:
            # 如果悬停超过5秒，则着陆
            if time.time() - hover_start_time > 5:
                control_drone("land")
                break  # 着陆后退出循环
    
    # 显示结果图像
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# 无人机着陆并退出
tello.land()
cap.release()
cv2.destroyAllWindows()
