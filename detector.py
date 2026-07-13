from collections import deque
import numpy as np
from config import WINDOW_SIZE, THRESHOLD

class OnlineZScoreDetector:
    def __init__(self):
        self.window = deque(maxlen=WINDOW_SIZE)

    def detect(self, value):
        self.window.append(value)
        if len(self.window) < WINDOW_SIZE:
            return False
        arr = np.array(self.window)
        mean = np.mean(arr)
        std = np.std(arr)
        if std == 0:
            return False
        z = (value - mean) / std
        return abs(z) > THRESHOLD
