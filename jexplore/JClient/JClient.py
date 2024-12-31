import json
import zmq
from jtop import jtop
from JClient.JConfig import JConfig
from JClient.JMeasure.JPower import JPower
from JClient.JMeasure.JMemory import JMemory

class JClient():
    def __init__(self):
        self.context = zmq.Context()
        self.get_tasks_socket = self.context.socket(zmq.PULL)
        self.get_tasks_socket.bind("tcp://*:6001")

        self.send_tasks_socket = self.context.socket(zmq.PUSH)
        self.send_tasks_socket.bind("tcp://*:6002")

        self.jc = JConfig('Orin')
        self.jc.read_config()

        self.jetson = jtop()
        self.JPower = JPower(self.jetson)
        self.JMemory = JMemory(self.jetson)

    def start_jtop(self):
        self.jetson.start()
    
    def close_jtop(self):
        self.jetson.close()

    def get_test(self):
        serialized_test_data = self.get_tasks_socket.recv_string()
        test_data = json.loads(serialized_test_data)
        return test_data
    
    def send_results(self, results):
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