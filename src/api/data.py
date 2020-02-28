import os 
import cv2
import random
from src.utils import augmentation, log, log_time

proportion_1 = 0.75
proportion_2 = 0.80
labels = ['saudavel', 'problemas', 'caruncho', 'ardido&mofado', 'manchado', 'mordido',
          'bandinha', 'contaminantes', 'genetico']

classifications = ['saudavel', 'ardido&mofado', 'bandinha', 'caruncho', 'contaminantes', 'genetico', 'manchado', 'mordido']
problems = ['ardido&mofado', 'bandinha', 'caruncho', 'contaminantes', 'genetico', 'manchado', 'mordido']

def normalization(path, destination, number):
    random_list = random.sample(range(0, len(os.listdir(path))), number)
    filename_list = os.listdir(path)
    for random_index in random_list:
        image = cv2.imread('{0}/{1}'.format(path, filename_list[random_index]))
        cv2.imwrite('{0}/{1}.jpg'.format(destination, 1 + len(os.listdir(destination))), image)

def from_output_transfer(path, destination):
    for filename in os.listdir(path):
        image = cv2.imread('{0}/{1}'.format(path, filename))
        cv2.imwrite('{0}/{1}.jpg'.format(destination, 1 + len(os.listdir(destination))), image)

def selection_network(labels, normalized_data, network_number):
    for label in labels:
        data_list = os.listdir('{0}/{1}'.format(normalized_data, label))
        random.shuffle(data_list)
        train_list = data_list[:int(0.8*len(data_list))]
        test_list = data_list[int(0.8*len(data_list)):]
        validation_list = test_list[int(0.75*len(test_list)):]
        test_list = test_list[:int(0.75*len(test_list))]
        k = 1
        for filename in train_list:
            image = cv2.imread('{0}/{1}/{2}'.format(normalized_data, label, filename))
            cv2.imwrite('data/images/train/{0}/{1}.{2}.jpg'.format(network_number, label, k), image)
            k+=1
        k = 1
        for filename in test_list:
            image = cv2.imread('{0}/{1}/{2}'.format(normalized_data, label, filename))
            cv2.imwrite('data/images/test/{0}/{1}.{2}.jpg'.format(network_number, label, k), image)
            k+=1
        k = 1
        for filename in validation_list:
            image = cv2.imread('{0}/{1}/{2}'.format(normalized_data, label, filename))
            cv2.imwrite('data/images/evaluation/{0}/{1}.jpg'.format(label, k), image)
            k+=1

if __name__=="__main__":
    image_path = 'data/images'
    try:
        os.makedirs('{}/train/network_1'.format(image_path))
    except:
        pass 
    try:
        os.makedirs('{}/train/network_2'.format(image_path))
    except:
        pass
    try:
        os.makedirs('{}/test/network_1'.format(image_path))
    except:
        pass
    try:
        os.makedirs('{}/test/network_2'.format(image_path))
    except:
        pass
    try:
        os.makedirs('{}/normalized'.format(image_path))
    except:
        pass
    
    try:
        os.makedirs('{}/normalized/problemas'.format(image_path))
    except:
        pass


    for label in labels:
        try:
            os.makedirs('{0}/evaluation/{1}'.format(image_path, label))
        except:
            pass
    for classification in classifications:
        try:
            os.makedirs('{0}/normalized/{1}'.format(image_path, classification))
        except:
            pass
    
    for classification in classifications:
        if classification == 'saudavel':
            number = 7*1200
        else:
            number = 1200
        original_path = '{0}/processed/{1}'.format(image_path, classification)
        destination_path = '{0}/normalized/{1}'.format(image_path, classification)
        if len(os.listdir(original_path)) < number: 
            augmentation(original_path, label, number)
            from_output_transfer('{}/output'.format(original_path), destination_path)
        else:
            normalization(original_path, destination_path, number)
    i = 1
    for problem in problems:
        for filename in os.listdir('{0}/normalized/{1}'.format(image_path, problem)):
            image = cv2.imread('{0}/normalized/{1}/{2}'.format(image_path, problem, filename))
            cv2.imwrite('{0}/normalized/problemas/{1}.png'.format(image_path, i), image)
            i+=1
    normalized_data = 'data/images/normalized'

    selection_network(['problemas', 'saudavel'], normalized_data, 'network_1')
    selection_network(['ardido&mofado', 'bandinha', 'caruncho', 'contaminantes', 'genetico', 'manchado', 'mordido']
    , normalized_data, 'network_2')
    