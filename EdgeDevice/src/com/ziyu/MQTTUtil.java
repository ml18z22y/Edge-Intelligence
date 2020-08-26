package com.ziyu;

import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class MQTTUtil {

    private static String tcpAddress;

    static {
        Properties brokerProp = new Properties();
        try {
            InputStream in = new BufferedInputStream(new FileInputStream("config/brokerConfig.properties"));
            brokerProp.load(in);
        } catch (IOException e) {
            e.printStackTrace();
        }
        tcpAddress = "tcp://" + brokerProp.getProperty("address") + ":" + brokerProp.getProperty("portNumber");
//        System.out.println(tcpAddress);
    }
    public static MqttClient Connect(String EdgeID, double LatencyWeight) throws MqttException, InterruptedException {
        System.out.println(EdgeID + " is connecting...");
        MqttClient client = new MqttClient(tcpAddress, EdgeID, new MemoryPersistence());
        MqttConnectOptions options = new MqttConnectOptions();
        options.setCleanSession(true);
        options.setUserName(EdgeID);
        options.setPassword("public".toCharArray());
        options.setConnectionTimeout(5);
        options.setKeepAliveInterval(20);
        client.connect(options);
        Thread.sleep((long) (1000 * LatencyWeight));
        client.setCallback(new EdgeCallBack(client));
        return client;
    }
    public static void Publish(MqttClient client, String topic, int qos, String payload, double latencyWeight) throws MqttException, InterruptedException {
        MqttMessage message = new MqttMessage((payload + "," + client.getClientId()).getBytes());
//        System.out.println(message.toString());
        message.setQos(qos);
        System.out.println(client.getClientId() + " starts to publish...");
        client.publish(topic, message);
        Thread.sleep((long) (1000 * latencyWeight));
    }
}
