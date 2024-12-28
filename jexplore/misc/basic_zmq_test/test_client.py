from JClient.JClient import JClient
import time

jclient = JClient()

for i in range(10):
    test_data = jclient.get_test()
    results = jclient.process_test(test_data)
    jclient.send_results(results)
    time.sleep(1)