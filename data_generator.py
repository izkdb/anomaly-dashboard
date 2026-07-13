import numpy as np
import time

def generate_data():
    t = 0
    while True:
        value = 10 * np.sin(t * 0.1) + np.random.normal(0, 1)
        if np.random.random() < 0.05:
            value += np.random.choice([-15, 15])
        yield t, value
        t += 1
        time.sleep(0.1)

