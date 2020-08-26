import platform
import subprocess
import re
import numpy as np
import random


def speed_test(address, n, l):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = "ping " + address + " " + "-n " + str(n) + " -l " + str(l)
    # print(command)
    p = subprocess.Popen(command,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    out = str(p.stdout.read().decode("gbk"))
    # print(out)
    reg = re.compile(r"\w*ms")
    time_list = reg.findall(out)
    # print(time_list)
    return time_list[:-3]


def prob_controller(x, percentage, index):
    if index != 0:  # judge if using CNN classifier
        return True
    y = 1-(0.2 * np.log(np.exp(9) - ((np.exp(5) - 1) * np.exp(4)) * x) - 0.8)
    if percentage >= y:
        return True
    else:
        item_list = [True, False]
        item_prob_list = [0.5, 0.5]
        rand = random.uniform(0, 1)
        cumulative_prob = 0.0
        for item, item_prob in zip(item_list, item_prob_list):
            cumulative_prob += item_prob
            if rand < cumulative_prob:
                break
        return item
