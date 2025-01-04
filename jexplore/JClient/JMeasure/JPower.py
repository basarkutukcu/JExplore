import numpy as np
from JClient.JMeasure.JMeasure import JMeasure

class JPower(JMeasure):
    
    def attach_measure_function(self):
        def read_measure(jetson):
            self.measure_list.append(jetson.power['tot']['power'])
        
        self.jetson.attach(read_measure)
    