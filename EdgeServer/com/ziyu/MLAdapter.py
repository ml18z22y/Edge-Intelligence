import com.ziyu.DNNDeployment as DNNDeployment
import com.ziyu.KNNDeployment as KNNDeployment
import com.ziyu.DTDeployment as DTDeployment


def classify(payload):
    # return DNNDeployment.classify(payload)
    return KNNDeployment.classify(payload)
    # return DTDeployment.classify(payload)
