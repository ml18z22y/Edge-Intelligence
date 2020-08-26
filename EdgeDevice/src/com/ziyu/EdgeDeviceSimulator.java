package com.ziyu;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;

import java.util.List;
import java.util.Random;

public class EdgeDeviceSimulator extends Thread{

    private String EdgeID;
    private List<String> RawData;
    private double LatencyWeight;
    private String Topic;

    public EdgeDeviceSimulator(String edgeID, List<String> rawData, double latencyWeight, String topic) {
        EdgeID = edgeID;
        RawData = rawData;
        LatencyWeight = latencyWeight;
        Topic = topic;
    }

    @Override
    public void run() {
        super.run();
        boolean correct = true;
        System.out.println(EdgeID + " is started.");
        MqttClient client = null;
        float lastTime = 0;
        float timeNumber = 0;
        int gap = 0;
        try {
            client = MQTTUtil.Connect(EdgeID, LatencyWeight);
        } catch (MqttException | InterruptedException e) {
            e.printStackTrace();
            System.out.println(EdgeID + " connection failed.");
            correct =false;
        }
        if(correct){
            System.out.println(EdgeID + " connected successfully.");
        }
        try {
            for(int i =0; i < RawData.size(); i++){
                timeNumber = Float.parseFloat(RawData.get(i).split(",")[0]); //get current data item time
                System.out.println("time number " + timeNumber);
                gap = (int) ((timeNumber - lastTime) * 1000); //calculate time interval
                if(gap != 0){
                    System.out.println("gap " + gap);
                    Thread.sleep(gap); //make the time sleep
                }
                MQTTUtil.Publish(client, Topic, 2, RawData.get(i), LatencyWeight); //publish message
                lastTime = timeNumber; //reset variable lastTime
            }
        } catch (MqttException | InterruptedException e) {
            e.printStackTrace();
            System.out.println(EdgeID + " connection failed.");
            correct = false;
        }
        if(correct){
            System.out.println(EdgeID + " published successfully.");
        }

    }
}
