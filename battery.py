from djitellopy import Tello
import time

# Tello 객체 생성 및 연결
tello = Tello()
tello.connect()

# 배터리 상태 출력
print(f"배터리 잔량: {tello.get_battery()}%")