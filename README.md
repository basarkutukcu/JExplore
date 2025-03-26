# jexplore

jexplore is a multi-client software/hardware design space exploration tool for Nvidia Jetson boards.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install jexplore in development mode.

```bash
pip install -e .
```

## Usage
### Host side

```python
from JHost.JHost import JHost
import time

client_list = {'Orin1': ('nvidia', 'orin1ip.ucsd.edu', 6001, 6002),
               'Orin2': ('nvidia', 'orin2ip.ucsd.edu', 6003, 6004)}

jhost = JHost(client_list=client_list)

test_configs = [{'config': (2, 2, 1, 10, 5, 3, 3, 0), 'sw_param1': 1},
                {'config': (4, 4, 1, 8, 5, 3, 3, 2), 'sw_param1': 2},
                {'config': (2, 2, 1, 10, 5, 4, 5, 3), 'sw_param1': 3},
                {'config': (4, 4, 4, 28, 28, 28, 10, 3), 'sw_param1': 4}]

for test_dict in test_configs:
    jhost.push_single_test(test_dict, client_name='Orin1')
    jhost.push_single_test(test_dict, client_name='Orin2')

    results1 = jhost.pull_test(client_name='Orin1')
    results2 = jhost.pull_test(client_name='Orin2')
    # use results to pick next config to test

jhost.save_results_to_csv('test_results.csv')
```

### Client side (client 1) - Jetson board

```python
from JClient.JClient import JClient
import time
from example_worklaods.test_workload import test_workload

meas_enable = {'power': True, 'memory': True, 'time': True}

jclient = JClient(device_name='Orin1', meas_enable=meas_enable, pull_port=6001, push_port=6002)

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

```

## Notes

* Make sure you push ssh key of host to client since the connection is made over ssh
* JClient needs root permissions since it changes the board's hardware configuration. JClient asks for sudo password after being launched.

## Citation

You can cite this work using:

```
@misc{kutukcu2025jexploredesignspaceexploration,
      title={JExplore: Design Space Exploration Tool for Nvidia Jetson Boards}, 
      author={Basar Kutukcu and Sinan Xie and Sabur Baidya and Sujit Dey},
      year={2025},
      eprint={2502.15773},
      archivePrefix={arXiv},
      primaryClass={cs.AR},
      url={https://arxiv.org/abs/2502.15773}, 
}
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
