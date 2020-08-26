package com.ziyu;

import org.eclipse.paho.client.mqttv3.*;

import java.sql.Timestamp;

public class EdgeCallBack implements MqttCallback {

    private MqttClient client;

    public EdgeCallBack(MqttClient client) {
        this.client = client;
    }

    @Override
    public void connectionLost(Throwable throwable) {
        System.out.print(client.getClientId() + " disconnected because of " + throwable + "...reconnecting...");
        try {
            client.reconnect();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void messageArrived(String s, MqttMessage mqttMessage) throws MqttException {
        String time = new Timestamp(System.currentTimeMillis()).toString();
        System.out.println(client.getClientId() + "got a message of topic " + s + "at " + time + ".");
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {
        System.out.println(client.getClientId() + " published a message successfully.");
    }
}
