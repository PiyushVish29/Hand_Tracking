import cv2
import mediapipe as mp
import math
import numpy as np
import screen_brightness_control as sbc   # ✅ FIXED

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_brightness = 0  # smoothing

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    lm_list = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            h, w, c = img.shape

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    if lm_list:
        # Thumb tip (4) and Index tip (8)
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]

        # Draw line
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cv2.circle(img, (x1, y1), 8, (255, 0, 255), -1)
        cv2.circle(img, (x2, y2), 8, (255, 0, 255), -1)

        # Distance
        length = math.hypot(x2 - x1, y2 - y1)

        # Map distance → brightness
        brightness = np.interp(length, [20, 200], [0, 100])
        brightness = int(brightness)

        # ✅ Smoothing (very important)
        if abs(brightness - prev_brightness) > 2:
            sbc.set_brightness(brightness)
            prev_brightness = brightness

        # UI bar
        bar = np.interp(brightness, [0, 100], [400, 150])

        cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 2)
        cv2.rectangle(img, (50, int(bar)), (85, 400), (0, 0, 255), -1)

        cv2.putText(img, f'{brightness} %', (40, 430),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Brightness Control", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()