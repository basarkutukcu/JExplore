import json
import zmq

class JClient():
    def __init__(self):
        self.context = zmq.Context()
        self.get_tasks_socket = self.context.socket(zmq.PULL)
        self.get_tasks_socket.bind("tcp://mesdatb.ucsd.edu:6001")

        self.send_tasks_socket = self.context.socket(zmq.PUSH)
        self.send_tasks_socket.bind("tcp://*:6002")

    def get_test(self):
        serialized_test_data = self.get_tasks_socket.recv_string()
        test_data = json.loads(serialized_test_data)
        return test_data
    
    def send_results(self, results):
        serialized_results = json.dumps(results)
        self.send_tasks_socket.send_string(serialized_results)

    def process_test(self, test_data):
        print(f"Processing test {test_data}")