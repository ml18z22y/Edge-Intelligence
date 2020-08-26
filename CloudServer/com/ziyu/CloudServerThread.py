import threading
import com.ziyu.MQTTUtil as Util
import com.ziyu.PlotFigureThread as PFThread


class CloudServerThread(threading.Thread):
    def __init__(self, serverID, tcp_address, port):
        threading.Thread.__init__(self)
        self.serverID = serverID
        self.tcp_address = tcp_address
        self.port = port

    def run(self):
        print("%s is started" % self.serverID)
        util = Util.MQTTUtil()
        client = util.connect(self.tcp_address, self.serverID, "EdgeDevice1", self.port)
        plot_figure = PFThread.PlotFigureThread(util)
        plot_figure.start()
        client.loop_forever()
