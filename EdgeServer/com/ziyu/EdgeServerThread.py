import threading
import com.ziyu.MQTTUtil as Util
import com.ziyu.Tool as tool
import numpy as np
import com.ziyu.RepeatTimer as RTimer


class EdgeServerThread(threading.Thread):

    def __init__(self, serverID, edge_address, cloud_address, port_number):
        threading.Thread.__init__(self)
        self.serverID = serverID
        self.edge_address = edge_address
        self.port_number = port_number
        self.cloud_address = cloud_address

    def run(self):
        print("%s is started" % self.serverID)
        util = Util.MQTTUtil()
        timer1 = RTimer.RepeatTimer(100.0, self.timer_for_std_mean, (util,))
        timer2 = RTimer.RepeatTimer(10, self.timer_for_state, (util,))
        timer1.start()
        timer2.start()
        client = util.connect(self.serverID, self.edge_address, self.cloud_address, self.port_number, 0.0, "ml18z22y")

    def timer_for_std_mean(self, util):
        print("in timer_for_std_mean now")
        # use ping command to evaluate the network status
        timeList = tool.speed_test(self.cloud_address, 15, 512)
        num_list = [float(timeList[i][:-2]) for i in range(len(timeList))]
        time_arr = np.array(num_list)
        # calculate long-term mean
        mean = np.mean(time_arr)
        # calculate standard deviation
        std = np.std(time_arr)
        print("in timer_for_std_mean now, new std %f and mean %f" % (std, mean))
        # update variables std and mean
        util.std = std
        util.mean = mean

    def timer_for_state(self, util):
        if util.std == -1. or util.mean == -1.:
            # util.state = -1.
            pass
        else:
            # use ping command to evaluate the network status
            time_list = tool.speed_test(self.cloud_address, 2, 512)
            short_mean_list = [float(time_list[i][:-2]) for i in range(len(time_list))]
            # calculate short-term mean
            short_mean = sum(short_mean_list) / len(short_mean_list)
            print("in timer_for_state now, new short_mean is %f" % short_mean)
            # calculate the short-term RRT deviation
            gap = short_mean - util.mean
            # print("gap: ", end="")
            # print(gap)
            # update network state index
            if gap > 0.0:
                util.state = gap / util.std
            else:
                util.state = -1