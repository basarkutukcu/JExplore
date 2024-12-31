import numpy as np
from JClient.JMeasure.JMeasure import JMeasure

class JMemory(JMeasure):
    
    def read_measure(self):
        self.measure_list.append(self.jetson.memory['RAM']['used'])