import paho.mqtt.client as mqtt


class MQTTUtil:
    def __init__(self):
        self.pre_list = []
        self.time_list = []
        self.name = "-1"
        self.colour_list = {
            1: "r",
            2: "b",
            3: "k",
            4: "g"
        }
        self.marker_list = {
            1: "^",
            2: "o",
            3: "v",
            4: "*"
        }
        self.class_list = ["sit on bed", "sit on chair" , "lying", "ambulating"]

    def connect(self, tcp_address, serverID, topic, port):
        client = mqtt.Client(serverID, True)
        client.username_pw_set(serverID, "public")
        client.on_connect = self.on_connect
        client.on_subscribe = self.on_subscribe
        client.on_message = self.on_message
        user_data = {
            "serverID": serverID,
            "topic": topic
        }
        client.user_data_set(user_data)
        client.connect(tcp_address, port)
        return client

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("%s connect to the cloud successfully." % userdata["serverID"])
            client.subscribe(userdata["topic"], 2)
        else:
            print("failed to connect to cloud server")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("%s subscribe successfully with qos %d" % (userdata["serverID"], granted_qos[0]))

    def on_message(self, client, userdata, message):
        print(
            "%s got a message: %s with topic %s" % (
                userdata["serverID"], str(message.payload, encoding="utf-8"), message.topic))
        message_list = [x.decode("ascii") for x in message.payload.split(b",")]
        print(message_list)
        self.time_list.append(float(message_list[0]))
        self.pre_list.append(int(message_list[-1]))
        self.name = message_list[-2]