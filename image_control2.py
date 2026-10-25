import cv2
import os
import numpy as np
import time
import math

def control(self, frame, lmList):

    if len(lmList) == 0:
        return self.display()

    x1, y1 = lmList[4][1], lmList[4][2]
    x2, y2 = lmList[8][1], lmList[8][2]

    distance = math.hypot(x2 - x1, y2 - y1)
    self.zoom(distance)

    self.move(x2, y2)

    # ---------- DELAY SETUP ----------
    if not hasattr(self, "last_switch"):
        self.last_switch = 0

    current_time = time.time()

    # ---------- GESTURE ----------
    if len(lmList) > 12:
        x3, y3 = lmList[12][1], lmList[12][2]
        dist2 = math.hypot(x3 - x2, y3 - y2)

        # NEXT IMAGE
        if dist2 < 40 and current_time - self.last_switch > 1:
            print("Next Image")
            self.next_image()
            self.last_switch = current_time

        # PREVIOUS IMAGE
        elif dist2 > 150 and current_time - self.last_switch > 1:
            print("Previous Image")
            self.prev_image()
            self.last_switch = current_time

    return self.display()
class ImageController:

    def __init__(self, folder_path):
        self.folder_path = r'C:\Users\24mc1\OneDrive\Pictures'
        self.image_list = os.listdir(r'C:\Users\24mc1\OneDrive\Pictures')
        self.index = 0

        self.load_image()

        self.scale = 1
        self.offset_x = 0
        self.offset_y = 0

    def load_image(self):
        path = os.path.join(self.folder_path, self.image_list[self.index])
        self.img_original = cv2.imread(path)

    def next_image(self):
        self.index = (self.index + 1) % len(self.image_list)
        self.load_image()

    def prev_image(self):
        self.index = (self.index - 1) % len(self.image_list)
        self.load_image()

    def zoom(self, distance):
        self.scale = max(0.5, min(distance / 300, 2))

    def move(self, x, y):
        self.offset_x = x
        self.offset_y = y

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

        x1 = max(0, min(self.offset_x, 800 - rw))
        y1 = max(0, min(self.offset_y, 600 - rh))

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

        
        x, y = lmList[8][1], lmList[8][2]
        self.move(x, y)

        canvas = self.display()

        return canvas if canvas is not None else frame