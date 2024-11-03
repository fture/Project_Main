import cv2
import time
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = HandDetector(maxHands=1)

hover_start_time = None

def control_drone(gesture):
    if gesture == "up":
        print("Gesture detected: Move Up")
    elif gesture == "down":
        print("Gesture detected: Move Down")
    elif gesture == "left":
        print("Gesture detected: Rotate Left")
    elif gesture == "right":
        print("Gesture detected: Rotate Right")
    elif gesture == "forward":
        print("Gesture detected: Move Forward")
    elif gesture == "back":
        print("Gesture detected: Move Back")
    elif gesture == "hover":
        print("Gesture detected: Hovering")
    elif gesture == "land":
        print("Gesture detected: Land")

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

        # 手势识别与模拟无人机控制
        if fingers == [1, 1, 1, 1, 1]:  # 所有手指伸开时前进
            control_drone("forward")
            hover_start_time = None  # 如果执行非悬停操作，则重置
        elif fingers == [0, 0, 0, 0, 0]:  # 所有手指收拢时后退
            control_drone("back")
            hover_start_time = None
        elif fingers == [0, 1, 0, 0, 0]:  # 仅食指伸开时上升
            control_drone("up")
            hover_start_time = None
        elif fingers == [0, 1, 1, 0, 0]:  # 食指和中指伸开时下降
            control_drone("down")
            hover_start_time = None
        elif fingers == [1, 0, 0, 0, 0]:  # 仅拇指伸开时左转
            control_drone("left")
            hover_start_time = None
        elif fingers == [0, 0, 0, 0, 1]:  # 仅小指伸开时右转
            control_drone("right")
            hover_start_time = None
    else:
        # 无法识别手部时悬停
        control_drone("hover")
        if hover_start_time is None:
            hover_start_time = time.time()  # 记录悬停开始时间
        else:
            # 如果悬停超过5秒，则着陆
            if time.time() - hover_start_time > 5:
                control_drone("land")
                break  # 着陆后结束循环
    
    # 显示结果图像
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
