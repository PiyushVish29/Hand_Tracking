import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, mode=False, maxHands=1, detectionCon=0.8, trackcon=0.8):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon              #con=confidence
        self.trackcon = trackcon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]  

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for landmark_one in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, landmark_one, self.mpHands.HAND_CONNECTIONS
                    )
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmarklist = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmarklist.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 5, (100, 0, 300), cv2.FILLED)

        return lmarklist

    def fingersUp(self, lmarklist):
        fingers = []

        if len(lmarklist) != 0:
            # Thumb
            if lmarklist[self.tipIds[0]][1] > lmarklist[self.tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Other fingers
            for id in range(1, 5):
                if lmarklist[self.tipIds[id]][2] < lmarklist[self.tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        return fingers