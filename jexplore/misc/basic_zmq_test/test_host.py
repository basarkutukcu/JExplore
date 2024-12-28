from JHost.JHost import JHost
import time

jhost = JHost()

for i in range(10):
    test_data = (i, i+1, i+2)
    jhost.push_single_test(test_data)
    print(f"Pushed test {test_data}")
    results = jhost.pull_test()
    print(f"Received results {results}")
