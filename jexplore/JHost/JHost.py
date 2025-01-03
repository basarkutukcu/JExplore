import json
import zmq
import zmq.ssh
import pandas as pd

class JHost():
    def __init__(self, client_list:list):
        '''
        client_list: list of dicts where keys are client_name and 
                    values are tuples of usernames, IP addresses and ports of corresponding clients'''
        self.client_list = client_list
        self.assigned_tasks_socket = {}
        self.finished_tasks_socket = {}
        self.context = zmq.Context()
        for client_name in self.client_list:
            client_user, client_ip, client_push_port, client_pull_port = self.client_list[client_name]
            self.assigned_tasks_socket[client_name] = self.context.socket(zmq.PUSH)
            zmq.ssh.tunnel_connection(self.assigned_tasks_socket[client_name], f"tcp://{client_ip}:{client_push_port}", f"{client_user}@{client_ip}")

            self.finished_tasks_socket[client_name] = self.context.socket(zmq.PULL)
            zmq.ssh.tunnel_connection(self.finished_tasks_socket[client_name], f"tcp://{client_ip}:{client_pull_port}", f"{client_user}@{client_ip}")


        # self.context = zmq.Context()
        # self.assigned_tasks_socket = self.context.socket(zmq.PUSH)
        # zmq.ssh.tunnel_connection(self.assigned_tasks_socket, "tcp://orinaiss.ucsd.edu:6001", "nvidia@orinaiss.ucsd.edu")

        # self.finished_tasks_socket = self.context.socket(zmq.PULL)
        # zmq.ssh.tunnel_connection(self.finished_tasks_socket, "tcp://orinaiss.ucsd.edu:6002", "nvidia@orinaiss.ucsd.edu")

        self.results = []

    def push_single_test(self, test_data:dict, client_name:str):

        '''Send a dict where
            test_data['config'] is config list
            And additional SW params as keys'''
        
        serialized_test_data = json.dumps(test_data)
        self.assigned_tasks_socket[client_name].send_string(serialized_test_data)

    def push_tests(self, multiple_test_data):
        pass

    def pull_test(self, client_name:str):

        '''Will receive a dict where
            result['test_data'] is the requested test_data
            result['metricX'] is the result for metricX'''
        
        serialized_results = self.finished_tasks_socket[client_name].recv_string()
        results_dict = json.loads(serialized_results)
        self.results.append(results_dict)
        return results_dict
    
    def save_results_to_csv(self, filename:str):
        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False, header=True, sep=',')
