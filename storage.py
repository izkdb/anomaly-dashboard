import pandas as pd
from collections import deque

class InMemoryStorage:
    def __init__(self, maxlen=1000):
        self.data = deque(maxlen=maxlen)

    def add(self, timestamp, value, is_anomaly):
        self.data.append({
            'timestamp': timestamp,
            'value': value,
            'anomaly': 1 if is_anomaly else 0
        })

    def get_dataframe(self):
        return pd.DataFrame(list(self.data))
