from abc import ABC, abstractmethod
import numpy as np

class JMeasure(ABC):
    def __init__(self, jetson):
        self.measure_list = []
        self.jetson = jetson
        self.read_measure = None
    
    @abstractmethod
    def attach_measure_function(self):
        pass
    
    def clean_measure_list(self):
        self.measure_list = []
    
    def get_measure_list(self):
        return self.measure_list
    
    def get_len_measure_list(self):
        return len(self.measure_list)
    
    def get_avg_measure(self):
        return np.mean(self.measure_list)
    
    def get_max_measure(self):
        return np.max(self.measure_list)
    
    def get_min_measure(self):
        return np.min(self.measure_list)
    
    def get_std_measure(self):
        return np.std(self.measure_list)