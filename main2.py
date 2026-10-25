import cv2
import math
from hand_tracker import HandTracker
from volume_control import VolumeController
from image_control import ImageController   

cap = cv2.VideoCapture(0)

detector = HandTracker()
volume = VolumeController()
imgCtrl = ImageController(r"C:\Users\24mc1\OneDrive\Pictures\Screenshots")   

mode = "volume"  

while True:

    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:

        fingers = detector.fingersUp(lmList)

        
        if fingers == [1, 1, 1, 1, 1]:
            mode = "image"

        elif fingers == [0, 1, 1, 0, 0]:
            mode = "volume"

    
        if mode == "volume":

            x1, y1 = lmList[4][1], lmList[4][2]   # thumb
            x2, y2 = lmList[8][1], lmList[8][2]   # index

            distance = math.hypot(x2 - x1, y2 - y1)

            volPercent = volume.set_volume_from_distance(distance)

            cv2.putText(img, f'Volume: {int(volPercent)}%',
                        (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 0),
                        3)

        # 👉 IMAGE CONTROL
        elif mode == "image":
            img = imgCtrl.control(img, lmList)   # call your image logic

        # 👉 SHOW MODE
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