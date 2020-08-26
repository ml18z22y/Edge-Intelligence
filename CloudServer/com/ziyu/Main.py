from xml.dom.minidom import parse
import com.ziyu.CloudServerThread as CT


def load_file():
    dom_tree = parse("../../config/brokerServer.XML")
    cloud_broker = dom_tree.getElementsByTagName("broker")[0]
    cloud_address = cloud_broker.getElementsByTagName("tcp_address")[0].firstChild.data
    port_number = cloud_broker.getElementsByTagName("port_number")[0].firstChild.data

    return cloud_address, port_number


cloud_address, port_number = load_file()
port_number = int(port_number)
number_of_threads = int(input("please input the number of edge servers: "))
cloud_thread = CT.CloudServerThread("CloudServer1", cloud_address, port_number)
cloud_thread.start()
