import numpy as np
from JClient.JMeasure.JMeasure import JMeasure

class JMemory(JMeasure):
    
    def read_measure(self):
        '''Append the used RAM in **bytes** to the measure list
            To get the used RAM in **MB** use the following formula:
            used_ram_MB = used_ram_bytes / 1024 / 1024'''
        self.measure_list.append(self.jetson.memory['RAM']['used'])