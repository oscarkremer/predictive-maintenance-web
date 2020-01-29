import os
import pickle
from abc import ABC, abstractmethod


class ModelTemplate(ABC):
    @abstractmethod
    def fit(self, data):
        """Used to train the model"""
        pass

    @abstractmethod
    def predict(self, days):
        """Used to predict products sales using the model"""
        pass

    def save(self, name):
        """Save model"""
        pickle.dump(self, open(self.model_filename(name), 'wb'))

    @classmethod
    def load(klass, name):
        """ Load the model """
        filename = klass().model_filename(name)
        if not os.path.exists(filename):
            return None
        return pickle.load(open(filename, 'rb'))
    
    def model_filename(self, name):
        self.name = type(self).__name__.lower()
        return "{0}/../../data/binary/models/{1}_{2}.pickle".format(os.path.dirname(__file__), self.name, name)
