from JHost.JHost import JHost
import time

jhost = JHost()

test_configs = [{'config': (2, 2, 1, 10, 5, 3, 3, 0), 'sw_param1': 1},
                {'config': (4, 4, 1, 8, 5, 3, 3, 2), 'sw_param1': 2},
                {'config': (2, 2, 1, 10, 5, 4, 5, 3), 'sw_param1': 3},
                {'config': (4, 4, 4, 28, 28, 28, 10, 3), 'sw_param1': 4}]



for test_dict in test_configs:
    jhost.push_single_test(test_dict)
    print(f"Pushed test {test_dict}")
    results = jhost.pull_test()
    print(f"Received results {results}")
