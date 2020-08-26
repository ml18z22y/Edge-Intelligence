package com.ziyu;

import java.io.IOException;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) throws IOException {
	// write your code here
        List<List<String>> dataList = DataLoader.LoadingData();
        String topic = "ml18z22y";
        System.out.println("Please input the number of edge devices:");
        Scanner scanner = new Scanner(System.in);
        int numberofThreads = scanner.nextInt();
        String [] EdgeDeviceList = new String [numberofThreads];
        double [] LatencyWeight = new double [numberofThreads];
        Random random = new Random();
        for(int i = 0; i<EdgeDeviceList.length; i++) {
            EdgeDeviceList[i] = "EdgeDevice" + (i + 1);
//            LatencyWeight[i] = random.nextDouble();
            LatencyWeight[i] = 0.0;
            System.out.println(EdgeDeviceList[i]);
        }
        for(int i = 0; i<EdgeDeviceList.length; i++){
            EdgeDeviceSimulator edgeThread = new EdgeDeviceSimulator(EdgeDeviceList[i], DataLoader.getSample(dataList), LatencyWeight[i], topic);
            edgeThread.start();
        }
    }
}
