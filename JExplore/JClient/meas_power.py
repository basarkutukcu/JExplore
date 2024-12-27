from jtop import jtop
import numpy as np

power_list = []
def read_power(jetson):
    global power_list
    power_list.append(jetson.power['tot']['power'])
    # power_list.append(jetson.power[0]['cur'])

jetson = jtop()
jetson.attach(read_power)

print('Measurement started - input something to stop...')
jetson.start()

_ = input()

jetson.close()

print(f'power list: {power_list}')
print(f'len of power measurements: {len(power_list)}')
print(f'avg_power: {np.mean(power_list)}')
print(f'max_power: {np.max(power_list)}')