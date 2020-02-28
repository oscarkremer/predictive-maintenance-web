import os
import pandas as pd
import numpy as np
import tensorflow as tf
from src.models import Classifier, Regressor
from src.utils.image_process import Segmentation, measure, size_analysis
from src.utils import path_helper, Path, suppress_stdout_stderr

'''
Definition of specialist for each type of beam, following the type
of identification, pushing the right structure and knowledge files
'''

class Beam:
    def __init__(self, type=0):
        self.type = '0'
        self.output_classes = [2, 7]
        paths = []
        paths.append(
            os.path.join(
                os.path.dirname(__file__),
                '../../data/knowledge/network_1/test.ckpt'))
        paths.append(
            os.path.join(
                os.path.dirname(__file__),
                '../../data/knowledge/network_2/test.ckpt'))
        self.path = paths
        self.labels = [['problemas',
                        'saudavel'],
                       ['ardido&mofado',
                        'bandinha',
                        'caruncho',
                        'contaminantes',
                        'genetico',
                        'manchado',
                        'mordido']]

    def analysis(self, predictions):
        net1 = np.array(predictions[0])
        net2 = np.array(predictions[1])
        result = np.zeros((net2.shape[0], 2))
        accuracy = np.zeros((net2.shape[0], 2))
        for j in range(net2.shape[0]):
            result[j][0] = net1[j].argmax()
            result[j][1] = net2[j].argmax()
            accuracy[j][0] = net1[j][net1[j].argmax()]
            accuracy[j][1] = net2[j][net2[j].argmax()]
        return result, accuracy

    def translate(self, predictions, names):
        pred_labels, health_names = [], []
        result, accuracy = self.analysis(predictions)
        for j in range(result.shape[0]):
            if int(result[j][0]) == 1:
                health_names.append(names[j])
                pred_labels.append(self.labels[0][1])
            else:
                pred_labels.append(self.labels[1][int(result[j][1])])
        return pred_labels, health_names

    def predict(self, data, names):
        with suppress_stdout_stderr():
            self.specialist = Classifier(self.path, self.output_classes)
            predictions = self.specialist.predict(data)
            pred_labels, health_names = self.translate(predictions, names)
            print(predictions)
            return predictions, pred_labels, health_names

    def geometric(self, path, healths):
        with suppress_stdout_stderr():        
            file_paths = []
            df = pd.DataFrame()
            size_12, size_11, size_10, size_9, size_0 = 0, 0, 0, 0, 0
            regressor = Regressor()
            regressor.load()
            for filename in healths: 
                width, height = measure(Segmentation('{0}/{1}.jpg'.format(path.image_processed, filename)))
                z = regressor.predict(width, height) 
                if size_analysis(width, height, z) == 12:
                    size_12+=1
                if size_analysis(width, height, z) == 11:
                    size_11+=1
                if size_analysis(width, height, z) == 10:
                    size_10+=1            
                if size_analysis(width, height, z) == 9:
                    size_9+=1
                if size_analysis(width, height, z) == 0:
                    size_0+=1    
            df['12'] = [size_12]
            df['11'] = [size_11]
            df['10'] = [size_10]
            df['9'] = [size_9]
            df['imaturo'] = [size_0]
            del regressor
            return df


