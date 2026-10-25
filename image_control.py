import cv2
import numpy as np
import math
import os
class ImageController:

    def __init__(self, img_path):
        self.img_original = cv2.imread("E:\WhatsApp Image 2026-03-27 at 20.51.44.jpeg")
        self.scale = 1
        self.move_horizontal = 0
        self.move_vertical = 0
        print(self.img_original)

    def zoom(self, distance):
        self.scale = max(0.5, min(distance / 300, 2))

    def move(self, x, y):
        self.move_horizontal = x
        self.move_vertical = y

    def display(self):

        if self.img_original is None:
            return None

        h, w, _ = self.img_original.shape

        new_w = int(w * self.scale)
        new_h = int(h * self.scale)


        new_w = min(new_w, 800)
        new_h = min(new_h, 600)

        resized = cv2.resize(self.img_original, (new_w, new_h))

        canvas = 255 * np.ones((600, 800, 3), dtype='uint8')

        rh, rw, _ = resized.shape

        x1 = max(0, min(self.move_horizontal, 800 - rw))
        y1 = max(0, min(self.move_vertical, 600 - rh))

        rh, rw, _ = resized.shape

        y2 = min(y1 + rh, 600)
        x2 = min(x1 + rw, 800)

        canvas[y1:y2, x1:x2] = resized[0:y2-y1, 0:x2-x1]

        return canvas

    
    def control(self, frame, lmList):

        if len(lmList) == 0:
            return self.display()

        
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        distance = math.hypot(x2 - x1, y2 - y1)
        self.zoom(distance)

        #postion chnge
        x, y = lmList[8][1], lmList[8][2]
        self.move(x, y)

        canvas = self.display()

        return canvas if canvas is not None else frame