import threading
import matplotlib.pyplot as plt
import numpy as np


class PlotFigureThread(threading.Thread):
    def __init__(self, util):
        threading.Thread.__init__(self)
        self.util = util

    def run(self):
        plt.ion()  # start figure interaction
        plt.figure(1)
        last_min = 0
        while True:
            min_length = min(len(self.util.pre_list), len(self.util.time_list))  # obtain the current list length
            if self.util.name != "-1" and min_length != last_min:  # if the list is updated
                new_pre_list = self.util.pre_list[last_min:]  # separate the new-arrived messages
                new_time_list = self.util.time_list[last_min:]
                for time, pre in zip(new_time_list, new_pre_list):  # plot the corresponding points
                    plt.ylim((0.5, 4.5))
                    new_ticks = np.linspace(1, 4, 4)
                    plt.yticks(new_ticks, self.util.class_list)
                    plt.scatter(time, pre, c=self.util.colour_list[pre], marker=self.util.marker_list[pre])
                    plt.xlabel("time (s)")
                    plt.ylabel("classification")
                    plt.pause(0.3)  # sleep the thread for 0.3 second
                last_min = min_length