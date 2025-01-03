from JClient.JClient import JClient
import time
from example_worklaods.test_workload import test_workload

meas_enable = {'power': True, 'memory': True, 'time': True}

jclient = JClient(device_name='Orin1', meas_enable=meas_enable)

jclient.start_jtop()

for i in range(4):
    test_data = jclient.get_test()
    config = test_data['config']
    sw_param1 = test_data['sw_param1']
    print(f'got config {config} with sw_param1 {sw_param1}')
    jclient.set_JConf(config)
    jclient.clean_and_start_measurements()
    
    test_workload()
    
    results = jclient.end_measurements()
    print(f"workload finished")
    results['config'] = config
    results['sw_param1'] = sw_param1
    jclient.send_results(results)

jclient.close_jtop()
