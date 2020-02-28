import os
import cv2
import numpy as np
from src.specialist.beam import Beam
from src.utils.analytics import make_dataframe, filter_dataframe
from src.utils.image_process import full_process, remove_emptyness
from src.utils.pre_process import break_data, input_data
from src.utils import Path

def classification(user_id, analysis_id):
    specialist = Beam()
    error, predictions, health_names = [], [], []
    path = Path(user_id, analysis_id)
    if os.listdir(path.image_processed):
        for filename in os.listdir(path.image_processed):
            os.remove('{0}/{1}'.format(path.image_processed, filename))
    for index, filename in enumerate(os.listdir(path.white_raw)):
        error.append(full_process('{0}/{1}'.format(path.white_raw, filename), path.image_processed, index+1))        
    if True in error:
        return 0, 0, 0, True
    else:
#        empty = remove_emptyness(path)

        empty = 0
        data, names = input_data(path.image_processed, path.processed)
        splited_data, splited_names = break_data(data, names, parts=2)
        for j in range(len(splited_data)):        
            _, prediction, health_name = specialist.predict(splited_data[j], splited_names[j])
            save_classified(prediction, splited_names[j], path)                
            predictions.append(prediction)
            health_names.append(health_name)
        geometric = specialist.geometric(path, np.concatenate((health_names[0], health_names[1])))
        dataframe = make_dataframe(path, np.concatenate((predictions[0], predictions[1])))
        result = filter_dataframe(dataframe)
        return result, geometric, empty, False

def save_classified(pred_labels, names, path):
    for i in range(len(names)):
        img = cv2.imread('{0}/{1}.jpg'.format(path.image_processed, names[i]))
        cv2.imwrite('{0}/{1}/{2}.jpg'.format(path.image_classified, pred_labels[i], names[i]), img)