import numpy as np
import time

class JTime():
    def __init__(self):
        self.start_time = 0
        self.end_time = 0

    def clean_and_start_measure(self):
        self.start_time = time.time()
        self.end_time = 0
    
    def end_measure(self):
        self.end_time = time.time()

    def get_measure(self):
        return self.end_time - self.start_time