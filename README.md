# Edge-Intelligence
The folder Classifier contains the CNN, DT and KNN implementation and training in three .ipynb files. You can inspect the model architectures especially CNN classifier.
The folder EdgeDevice contains the IoT tier impplementation in Java. Note that data set is needed for running which you could download from UCI Machine Learning Repository and copy to the folder named "dataset": https://archive.ics.uci.edu/ml/datasets/Activity+recognition+with+healthy+older+people+using+a+batteryless+wearable+sensor.
The folder EdgeServer and CloudServer contain the code implementation of edge node tier and Cloud tier respectively. Both are programmed in Python.
The related MQTT broker key words are listed below:
  EdgeDevice:
      username="EdgeDevice" + current edge device simulation thread number
      password="public"
      topic="ml18z22y"
  EdgeServer:
      username="EdgeServer" + current edge server simulation thread number
      password="public"
      topic="ml18z22y"
  CloudServer:
      username="CloudServer" + current Cloud server simulation thread number
      password="public"
      topic="ml18z22y"
