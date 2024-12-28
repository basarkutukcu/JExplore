from JClient.JClient import JClient
import time
from example_worklaods.test_workload import test_workload

jclient = JClient()


while True:
    test_data = jclient.get_test()
    config = test_data['config']
    sw_param1 = test_data['sw_param1']
    print(f'got config {config} with sw_param1 {sw_param1}')
    jclient.set_JConf(config)
    test_workload()
    print(f"workload finished")
    results = {'config': config, 'result': sw_param1+1}
    jclient.send_results(results)
