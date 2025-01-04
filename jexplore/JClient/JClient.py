import json
import zmq
from jtop import jtop
from JClient.JConfig import JConfig
from JClient.JMeasure.JPower import JPower
from JClient.JMeasure.JMemory import JMemory
from JClient.JMeasure.JTime import JTime

class JClient():
    def __init__(self, device_name:str, meas_enable:dict, device_type='Orin', pull_port=6001, push_port=6002):
        self.device_name = device_name
        self.device_type = device_type

        self.context = zmq.Context()
        self.get_tasks_socket = self.context.socket(zmq.PULL)
        self.get_tasks_socket.bind(f"tcp://*:{pull_port}")

        self.send_tasks_socket = self.context.socket(zmq.PUSH)
        self.send_tasks_socket.bind(f"tcp://*:{push_port}")

        self.jc = JConfig(device_type)
        self.jc.read_config()

        self.meas_enable = meas_enable

        self.jetson = jtop()
        if self.meas_enable['power']:
            self.JPower = JPower(self.jetson)
            self.JPower.attach_measure_function()
            print(f"Power measurement enabled")
        if self.meas_enable['memory']:
            self.JMemory = JMemory(self.jetson)
            self.JMemory.attach_measure_function()
            print(f"Memory measurement enabled")
        if self.meas_enable['time']:
            self.JTime = JTime()
            print(f"Time measurement enabled")

    def clean_and_start_measurements(self):
        if self.meas_enable['power']:
            self.JPower.clean_measure_list()
        if self.meas_enable['memory']:
            self.JMemory.clean_measure_list()
        if self.meas_enable['time']:
            self.JTime.clean_and_start_measure()

    def end_measurements(self):
        meas_results = {}
        if self.meas_enable['power']:
            meas_results['power'] = self.JPower.get_avg_measure()
        if self.meas_enable['memory']:
            meas_results['memory'] = self.JMemory.get_avg_measure()
        if self.meas_enable['time']:
            self.JTime.end_measure()
            meas_results['time'] = self.JTime.get_measure()
        
        return meas_results


    def start_jtop(self):
        self.jetson.start()
    
    def close_jtop(self):
        self.jetson.close()

    def get_test(self):
        serialized_test_data = self.get_tasks_socket.recv_string()
        test_data = json.loads(serialized_test_data)
        return test_data
    
    def send_results(self, results):
        results['device_name'] = self.device_name
        results['device_type'] = self.device_type
        serialized_results = json.dumps(results)
        self.send_tasks_socket.send_string(serialized_results)

    def process_test(self, test_data):
        print(f"Processing test {test_data}")
        processed_data = {}
        processed_data['test_data'] = test_data
        processed_data['metric1'] = 1
        processed_data['metric2'] = 2
        return processed_data
        
    def set_JConf(self, conf):
        conf = tuple(conf)
        print(f"Setting conf {conf}")
        self.jc.set_confs(conf)

    def set_max_config(self):
        print(f"Setting max")
        conf = (-1, -1, -1, -1, -1, -1, -1, -1)
        self.jc.set_confs(conf)