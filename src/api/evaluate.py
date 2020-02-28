from sklearn.metrics import confusion_matrix
from src.specialist.beam import Beam
from src.utils import log, log_time
from src.utils.pre_process import break_data, input_data

def evaluate_network(labels, result_labels):
    prediction_label, right_label = [], []
    for i, label in enumerate(labels):
        right, wrong = 0, 0
        specialist = Beam()
        data, names = input_data('data/images/evaluation/{0}'.format(label),'')
        splited_data, splited_names = break_data(data, names, parts=2)
        for j in range(len(splited_data)):        
            _, predictions,_ = specialist.predict(splited_data[j], splited_names[j])
            for prediction in predictions:
                right_label.append(label)
                if label=='problemas' and prediction!='saudavel':
                    prediction_label.append('problemas')
                else:
                    prediction_label.append(prediction)
                if prediction in result_labels[i]:
                    right+=1
                else:
                    wrong+=1   
        log('{0} --- Right: {1} - Wrong: {2}'.format(labels[i], right, wrong))
    print(confusion_matrix(right_label, prediction_label, labels=labels))

if __name__ == '__main__':
    labels = [['saudavel', 'problemas'],
        ['saudavel', 'caruncho', 'ardido&mofado', 'manchado', 'mordido', 'bandinha', 'contaminantes', 'genetico']]
    result_labels =  [[['saudavel'],['caruncho', 'ardido&mofado', 'manchado', 'mordido',
            'bandinha', 'contaminantes', 'genetico']],[['saudavel'], ['caruncho'], ['ardido&mofado'], ['manchado'], ['mordido'],
            ['bandinha'], ['contaminantes'], ['genetico']]]
    with log_time('Evaluation for Convolutional Networks '):
        for i in range(len(labels)):
            evaluate_network(labels[i], result_labels[i])
    
