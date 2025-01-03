from JHost.JHost import JHost
import time

client_list = {'Orin1': ('nvidia', 'orinaiss.ucsd.edu', 6001, 6002),
               'Orin2': ('nvidia', 'xavieraiss.ucsd.edu', 6003, 6004)}

jhost = JHost(client_list=client_list)

test_configs = [{'config': (2, 2, 1, 10, 5, 3, 3, 0), 'sw_param1': 1},
                {'config': (4, 4, 1, 8, 5, 3, 3, 2), 'sw_param1': 2},
                {'config': (2, 2, 1, 10, 5, 4, 5, 3), 'sw_param1': 3},
                {'config': (4, 4, 4, 28, 28, 28, 10, 3), 'sw_param1': 4}]



for test_dict in test_configs:
    jhost.push_single_test(test_dict, client_name='Orin1')
    print(f"Pushed test {test_dict}")
    results = jhost.pull_test(client_name='Orin1')
    print(f"Received results {results}")

jhost.save_results_to_csv('test_results.csv')
