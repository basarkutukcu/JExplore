import json
import zmq

class JHost():
    def __init__(self):
        self.context = zmq.Context()
        self.assigned_tasks_socket = self.context.socket(zmq.PUSH)
        self.assigned_tasks_socket.bind("tcp://*:6001")

        self.finished_tasks_socket = self.context.socket(zmq.PULL)
        self.finished_tasks_socket.bind("tcp://*:6002")

        self.results = {}

    def push_single_test(self, test_data:tuple):
        
        serialized_test_data = json.dumps(test_data)
        self.assigned_tasks_socket.send_string(serialized_test_data)

    def push_tests(self, multiple_test_data):
        pass

    def pull_test(self):

        '''Will receive a dict where
            result['test_data'] is the requested test_data
            result['metricX'] is the result for metricX'''
        
        serialized_results = self.finished_tasks_socket.recv_string()
        results = json.loads(serialized_results)
        return results
