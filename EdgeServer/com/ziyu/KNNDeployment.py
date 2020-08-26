import pickle
import numpy as np


def classify(raw_data):
    data_list = [float(raw_data[i]) for i in range(len(raw_data) - 2)]
    data_list = np.array(data_list)
    # print(data_list)
    model = pickle.load(open("../../model/KNN.pickle", "rb"))
    # print("after load")
    data_list = np.expand_dims(data_list, 0)
    # print(data_list)
    prediction = model.predict(data_list)
    # print(prediction)
    return prediction[0], -1, 1
