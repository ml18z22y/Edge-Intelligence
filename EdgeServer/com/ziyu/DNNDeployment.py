from com.ziyu.DNNAlgorithm import Model, DHOP
import torch
import pandas as pd
import torch.nn.functional as f


def classify(raw_data):
    data_list = [float(raw_data[i]) for i in range(len(raw_data) - 1)]
    values = []
    classes = []
    model = Model()
    model = model.double()
    model.load_state_dict(torch.load("../../model/DNNmodel_old.pt", map_location="cpu"))
    values.append(data_list[0:-1])
    classes.append(int(data_list[-1])-1)
    data = {
            "value": values,
            "class": classes
    }
    data_df = pd.DataFrame(data, columns=["value", "class"])
    DHOP_data = DHOP(df=data_df)
    classify_loader = torch.utils.data.DataLoader(
        DHOP_data,
        batch_size=1,
        shuffle=False
    )
    for i, data in enumerate(classify_loader, 0):
        value_i, class_i = data
        output = model(value_i)
        _, prediction = torch.max(output.detach(), 1)
        percentage = f.softmax(output.detach(), dim=1).float().numpy()
        prediction = prediction.numpy()
        percentage = percentage[0][prediction[0]]
        print(prediction + 1)
        # print(percentage)
        # print(class_i)
        return prediction[0], percentage, 0
