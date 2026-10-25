import cv2
import math
from hand_tracker import HandTracker
from volume_control import VolumeController
from image_control2 import ImageController2

cap = cv2.VideoCapture(0)

detector = HandTracker()
volume = VolumeController()
controller = ImageController2("images")

while True:

    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:

        # Thumb & Index
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        distance = math.hypot(x2 - x1, y2 - y1)

        # ------------------ GESTURE MODES ------------------

        # 👉 SMALL DISTANCE → VOLUME CONTROL
        if distance < 50:
            volPercent = volume.set_volume_from_distance(distance)

            cv2.putText(img, f'Volume: {int(volPercent)}%',
                        (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 0),
                        3)

        # 👉 OTHERWISE → IMAGE CONTROL
        else:
            img = controller.control(img, lmList)

    # Show image viewer (IMPORTANT)
    canvas = controller.display()
    if canvas is not None:
        cv2.imshow("Image Viewer", canvas)

    cv2.imshow("Webcam", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
