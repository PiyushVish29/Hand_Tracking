import cv2
import math
import time
from hand_tracker import HandTracker
from volume_control import VolumeController
from image_control import ImageController
from brightness_control import BrightnessController

cap = cv2.VideoCapture(0)

detector = HandTracker()
volume = VolumeController()
brightness = BrightnessController()
imgCtrl = ImageController(r"C:\Users\24mc1\OneDrive\Pictures\Screenshots")

mode = "volume"

# 👉 ADD THIS (for stability)
last_switch = 0
switch_delay = 1  # seconds

while True:

    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:

        fingers = detector.fingersUp(lmList)

        # 👉 DEBUG (remove later if you want)
        # print(fingers)

        current_time = time.time()

        # ================= SMART MODE SWITCH =================
        if current_time - last_switch > switch_delay:

            # 🖐️ Open hand → IMAGE
            if sum(fingers) == 5:
                mode = "image"
                last_switch = current_time

            # ✌️ Two fingers → VOLUME
            elif fingers[1] == 1 and fingers[2] == 1 and sum(fingers) == 2:
                mode = "volume"
                last_switch = current_time

            # ☝️ Index only → BRIGHTNESS
            elif fingers[1] == 1 and sum(fingers) == 1:
                mode = "brightness"
                last_switch = current_time

        # ================= COMMON POINTS =================
        x1, y1 = lmList[4][1], lmList[4][2]   # thumb
        x2, y2 = lmList[8][1], lmList[8][2]   # index
        distance = math.hypot(x2 - x1, y2 - y1)
        print(fingers)

        # ================= VOLUME =================
        if mode == "volume":

            volPercent = volume.set_volume_from_distance(distance)

            cv2.putText(img, f'Volume: {int(volPercent)}%',
                        (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 0),
                        3)

        # ================= BRIGHTNESS =================
        elif mode == "brightness":

            brightPercent = brightness.set_brightness_from_distance(distance)

            cv2.putText(img, f'Brightness: {int(brightPercent)}%',
                        (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3)

        # ================= IMAGE =================
        elif mode == "image":
            img = imgCtrl.control(img, lmList)

        # ================= MODE DISPLAY =================
        cv2.putText(img, f'Mode: {mode.upper()}',
                    (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3)

    cv2.imshow("result", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
