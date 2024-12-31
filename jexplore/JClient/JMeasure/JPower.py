import numpy as np
from JClient.JMeasure.JMeasure import JMeasure

class JPower(JMeasure):
    
    def read_measure(self):
        self.measure_list.append(self.jetson.power['tot']['power'])
    