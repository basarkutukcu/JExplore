import json
import zmq
import zmq.ssh

class JHost():
    def __init__(self):
        self.context = zmq.Context()
        self.assigned_tasks_socket = self.context.socket(zmq.PUSH)
        zmq.ssh.tunnel_connection(self.assigned_tasks_socket, "tcp://orinaiss.ucsd.edu:6001", "nvidia@orinaiss.ucsd.edu")

        self.finished_tasks_socket = self.context.socket(zmq.PULL)
        zmq.ssh.tunnel_connection(self.finished_tasks_socket, "tcp://orinaiss.ucsd.edu:6002", "nvidia@orinaiss.ucsd.edu")

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
