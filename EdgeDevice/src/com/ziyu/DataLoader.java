package com.ziyu;

import org.omg.PortableInterceptor.SYSTEM_EXCEPTION;

import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public class DataLoader {

    public static List<List<String>> LoadingData() throws IOException {
        String path = "dataset";
        File file = new File(path);
        File [] dataFiles = file.listFiles();
        List<List<String>> dataList = new ArrayList<>();
        for(int i =0; i<dataFiles.length; i++){
            List<String> dataset = new ArrayList<>();
            StringBuffer stringBuffer;
            int addition = 0;
            InputStreamReader reader = new InputStreamReader(new FileInputStream(dataFiles[i]));
            BufferedReader br = new BufferedReader(reader);
            String line = br.readLine();
            while(line != null){
                if (dataFiles[i].toString().toCharArray()[dataFiles[i].toString().length()-1] == 'M'){
                    addition = 1;
                }
//                System.out.println(line);
                stringBuffer = new StringBuffer(line);
                stringBuffer.insert(line.length() - 1, addition + ",");
                line = stringBuffer.toString();
//                System.out.println(line);
                dataset.add(line);
                line = br.readLine();
            }
            dataList.add(dataset);
        }
//        Collections.shuffle(dataList);
        return dataList;
    }

    public static List<String> getSample(List<List<String>> dataList){
        Random random = new Random();
//        int index = random.nextInt(dataList.size());
        int index = 3;
        List<String> sample = dataList.get(index);
        System.out.println(index);
        int count1 = 0;
        int count2 = 0;
        int count3 =0;
        int count4 = 0;
        int classification;
        for(int i=0;i<sample.size();i++){
            String [] to_list = sample.get(i).split(",");
            classification = Integer.parseInt(to_list[to_list.length-1]);
            switch (classification){
                case 1:
                    count1++;
                    break;
                case 2:
                    count2++;
                    break;
                case 3:
                    count3++;
                    break;
                case 4:
                    count4++;
                    break;
            }
        }
        System.out.println(count1 / count4 + " " + count2 / count4+ " " + count3 / count4+ " " + count4 / count4);
        return sample;
    }

    public static void main(String[] args) throws Exception {
        getSample(LoadingData());
    }

}
