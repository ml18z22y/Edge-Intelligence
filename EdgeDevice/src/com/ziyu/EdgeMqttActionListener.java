package com.ziyu;

import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttToken;

public class EdgeMqttActionListener implements IMqttActionListener {
    private String EdgeID;

    public EdgeMqttActionListener(String edgeID) {
        EdgeID = edgeID;
    }

    @Override
    public void onSuccess(IMqttToken iMqttToken) {
        System.out.println(EdgeID + "connected successfully");
    }

    @Override
    public void onFailure(IMqttToken iMqttToken, Throwable throwable) {
        System.out.println(EdgeID + "connection failed");
    }
}
