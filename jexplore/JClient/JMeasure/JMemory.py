import numpy as np
from JClient.JMeasure.JMeasure import JMeasure

class JMemory(JMeasure):
    
    def read_measure_wrapper(self):
        '''Append the used RAM in **bytes** to the measure list
            To get the used RAM in **MB** use the following formula:
            used_ram_MB = used_ram_bytes / 1024 / 1024'''
        def read_measure(jetson):
            self.measure_list.append(jetson.memory['RAM']['used'])
        
        self.jetson.attach(read_measure)