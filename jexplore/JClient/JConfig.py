import configparser
import subprocess
import sys
sys.path.insert(0,'./')
#[40800000, 68000000, 102000000, 
                    # 204000000, 408000000, 665600000, 
                    # 800000000, 1062400000, 1331200000, 
                    # 1600000000, 1866000000]
freq_dict = {'emc': [204000000, 665600000,
                    2133000000, 3200000000],
            'cpu': [115200, 192000, 268800, 345600, 422400, 
                    499200, 576000, 652800, 729600, 806400, 
                    883200, 960000, 1036800, 1113600, 1190400, 
                    1267200, 1344000, 1420800, 1497600, 1574400, 
                    1651200, 1728000, 1804800, 1881600, 1958400, 
                    2035200, 2112000, 2188800, 2201600],
            'gpu': [306000000, 408000000, 510000000, 612000000,
                    714000000, 816000000, 918000000, 1020000000, 
                    1122000000, 1224000000, 1300500000]}

class JConfig():
    def __init__(self, j_type):
        self.j_type = j_type
        self.config_dict = None

    def read_config(self):
        cp = configparser.ConfigParser()
        cp.read('jconfig.cfg')
        self.config_dict = dict(cp.items(self.j_type))

    def state_cpu(self, core_num, state):
        """ 
        core_num (int) can be 0:3 or 0:1 
        state (int) can be 0 or 1
        """
        name = f'cpu_core_{core_num}_on_addr'
        addr = self.config_dict[name]
        cmd = f'echo {state} > {addr}'
        _ = subprocess.Popen(cmd, shell=True).wait()


    def freq_cpu_gpu(self, htype, freq_no, cpu_cluster_no=0):       
        min_addr = self.config_dict[f'{htype}_c{cpu_cluster_no}_min_freq']
        max_addr = self.config_dict[f'{htype}_c{cpu_cluster_no}_max_freq']
        freq_list = freq_dict[htype]

        # set scaling freqs to max in correct order
        cmd = f'echo {freq_list[-1]} > {max_addr}'
        _ = subprocess.Popen(cmd, shell=True).wait()
        cmd = f'echo {freq_list[-1]} > {min_addr}'
        _ = subprocess.Popen(cmd, shell=True).wait()


        # set scaling freqs to desired value in correct order
        cmd = f'echo {freq_list[freq_no]} > {min_addr}'
        _ = subprocess.Popen(cmd, shell=True).wait()
        cmd = f'echo {freq_list[freq_no]} > {max_addr}'
        _ = subprocess.Popen(cmd, shell=True).wait()

    def freq_emc(self, freq_no):
        ratelock_addr = self.config_dict['emc_ratelock']
        emc_state = self.config_dict['emc_state']
        emc_rate = self.config_dict['emc_rate']

        freq_list = freq_dict['emc']

        cmd = f'echo 1 > {ratelock_addr}'
        _ = subprocess.Popen(cmd, shell=True).wait()
        cmd = f'echo 1 > {emc_state}'
        _ = subprocess.Popen(cmd, shell=True).wait()
        cmd = f'echo {freq_list[freq_no]} > {emc_rate}'
        _ = subprocess.Popen(cmd, shell=True).wait()

    def expand_core_num(self, core_num):
        exp_core = []
        for i in range(4):
            if i < core_num:
                exp_core.append(1)
            else:
                exp_core.append(0)

        return exp_core

    def jetson_clocks(self):
        _ = subprocess.Popen('jetson_clocks', shell=True).wait()

    def set_confs(self, confs):
        # Warning: It can give a harmless IO error when try to assign freq to offline CPU cores
        c0 = confs[0]
        c1 = confs[1]
        c2 = confs[2]
        f0 = confs[3]
        f1 = confs[4]
        f2 = confs[5]
        gf = confs[6]
        ef = confs[7]

        expanded_c0 = self.expand_core_num(c0)
        expanded_c1 = self.expand_core_num(c1)
        expanded_c2 = self.expand_core_num(c2)
        total_cores = expanded_c0 + expanded_c1 + expanded_c2
        print(total_cores)
        for i,onl in enumerate(total_cores):
            self.state_cpu(i, onl)

        self.freq_cpu_gpu('cpu', f0, 0)
        self.freq_cpu_gpu('cpu', f1, 1)
        self.freq_cpu_gpu('cpu', f2, 2)

        self.freq_cpu_gpu('gpu', gf)

        self.freq_emc(ef)

if __name__ == "__main__":

    jc = JConfig('Orin')
    jc.read_config()

    confs = (2, 2, -1, 10, 5, -1, 3, 0)
    jc.set_confs(confs)

