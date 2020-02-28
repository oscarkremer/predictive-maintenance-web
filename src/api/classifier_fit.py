import sys
import os
import argparse
from src.models.classifier_model import TF_classifier
from src.utils import path_helper, log, log_time
from src.utils.pre_process import train_data, input_data


def train(folder_path, save_path, network_id, epochs):    
    label_general = ['problemas', 'saudavel']
    label_problem = ['ardido&mofado', 'bandinha', 'caruncho', 'contaminantes', 'genetico', 'manchado', 'mordido']
    labels = [label_general, label_problem]
    train_size = [10000, 6160]
    log('Processing data for training - Train Data ' + label_log(labels[network_id-1]))
    
    train = train_data('{0}/train/network_{1}'.format(folder_path, network_id), 
                    '{0}/network_{1}'.format(save_path, network_id), labels[network_id-1])
    log('Processing data for training - Test Data ' + label_log(labels[network_id-1]))
    test = train_data('{0}/test/network_{1}'.format(folder_path, network_id), 
                    '{0}/network_{1}'.format(save_path, network_id), labels[network_id-1])
    log('Training to differenciate between ' + label_log(labels[network_id-1]))
    classifier = TF_classifier(len(labels[network_id-1]))
    classifier.train(train, test, train_size[network_id-1], epochs=epochs, retrain=False)

def label_log(labels):
    sentence = ''
    for label in labels:
        sentence += '-' + label
    return sentence

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    data_path = os.path.join(os.path.dirname(__file__), '../../data/images')
    save_path = os.path.join(os.path.dirname(__file__), '../../data/processed/train')
    parser.add_argument('--epochs', default=10, type=int)
    parser.add_argument('--network-id', default=1, type=int)
    args = parser.parse_args()
    with log_time('Training'):
        train(data_path, save_path, network_id = args.network_id, epochs=args.epochs)
