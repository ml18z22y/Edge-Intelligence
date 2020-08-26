import paho.mqtt.client as mqtt
import com.ziyu.MLAdapter as MLAdapter
import com.ziyu.Tool as tool


class MQTTUtil:
    def __init__(self):
        self.std = -1.
        self.mean = -1.
        self.state = -1.

    def on_connect(self, client, userdata, flags, rc):
        # print("on connect")
        if rc == 0:
            print("%s connected successfully." % userdata["serverID"])
            mid = client.subscribe(userdata["topic"], 2)
            userdata["mid"] = mid
            client.user_data_set(userdata)
        else:
            print("%s connected failed because of %d." % (userdata["serverID"], rc))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        if userdata["mid"][0] is not 0:
            exit(-1)
        if mid is userdata["mid"][1]:
            print("%s subscribed successfully with qos %d." % (userdata["serverID"], granted_qos[0]))
        else:
            print("%s subscription failed." % userdata["serverID"])

    def on_message(self, client, userdata, message):
        print(
            "%s got a message: %s with topic %s" % (
                userdata["serverID"], str(message.payload, encoding="utf-8"), message.topic))
        # DNNDeployment.classify(message.payload)
        payload = message.payload.split(b",")
        # print(payload)
        client_publish = userdata["client_publish"]
        topic = payload[-1].decode("ascii")
        # print("before classify")
        # print("before classify")
        prediction, percentage, index = MLAdapter.classify(payload)
        # print("after classify")
        # print(prediction)
        del payload[-2:-1]
        filter_list = []  # ban-list initialisation
        round_number = float(int(self.state))  # get the integer part of member variable state
        if round_number >= -1.:  # add lying-on-bed class into the ban-list
            filter_list.append(2)
        if round_number >= 1.:  # add sitting-on-bed class into the ban-list
            filter_list.append(0)
        if round_number >= 2.:  # add sitting-on-chair class into the ban-list
            filter_list.append(1)
        baseline = True
        if baseline is False:
            if prediction not in filter_list:  # intercept data items in the ban-list
                if prediction != 3:  # judge if the data item belongs to class ambulating
                    # invoke possibility controller to determine whether to send
                    if tool.prob_controller(self.state - round_number, percentage, index):
                        payload_str = cat_string(payload, prediction)
                        client_publish.publish(topic, payload_str, qos=2)
                else:
                    payload_str = cat_string(payload, prediction)
                    client_publish.publish(topic, payload_str, qos=2)
        else:
            payload_str = cat_string(payload, prediction)
            client_publish.publish(topic, payload_str, qos=2)


    def connect(self, serverID, tcp_address, cloud_address, port, latency_weight, topic):
        client_publish = mqtt.Client(serverID, True)
        client_publish.username_pw_set(serverID, "public")
        client_publish.user_data_set(serverID)
        client_publish.on_connect = on_connect_for_publish
        client_publish.on_publish = on_publish_for_publish
        client_publish.connect(cloud_address, port)
        # print(serverID + "connect to cloud broker successfully.")
        client_publish.loop_start()
        # print("after loop")
        user_data = {
            "serverID": serverID,
            "topic": topic,
            "cloud_address": cloud_address,
            "client_publish": client_publish
        }
        client = mqtt.Client(serverID, True)
        client.user_data_set(user_data)
        client.username_pw_set(serverID, "public")
        client.on_connect = self.on_connect
        client.on_subscribe = self.on_subscribe
        client.on_message = self.on_message
        client.connect(tcp_address, port)
        client.loop_forever()
        return client


def cat_string(array, prediction):
    cat_list = [x.decode("ascii") for x in array]
    cat_list.append(str(prediction + 1))
    # print(cat_list)
    cat_str = ",".join(cat_list)
    # print(cat_str)
    return cat_str


def on_connect_for_publish(client, userdata, flags, rc):
    if rc == 0:
        print(userdata + " connect to cloud successfully")


def on_publish_for_publish(client, userdata, mid):
    print(userdata + " publish to cloud successfully")
