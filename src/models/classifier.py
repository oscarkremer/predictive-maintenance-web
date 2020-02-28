import numpy as np
from .classifier_model.model import TF_classifier


class Classifier:
    def __init__(self, paths, output_classes):
        self.paths = paths
        self.output_classes = output_classes

    def predict(self, data):
        final_prediction = []
        for i in range(len(self.paths)):
            classifier = TF_classifier(self.output_classes[i])
            prediction = classifier.predict(data, self.paths[i])
            final_prediction.append(prediction)
        return final_prediction
