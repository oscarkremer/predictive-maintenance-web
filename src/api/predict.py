import os
import cv2
import pandas as pd
from src.utils import Path
from src.utils.image_process import full_process
from src.utils.visualization import image_grid
from src.utils.pre_process import input_data
from src.specialist.beam import Beam
LABELS = ['saudavel', 'caruncho', 'ardido&mofado', 'manchado', 'mordido', 'bandinha', 
            'contaminantes', 'genetico']

def main(client_id, analysis_id):
    path = Path(client_id, analysis_id)
    full_process(path.image_raw + '/image.png', path.image_processed)
    make_predict(path)

def make_predict(path):
    data, names = input_data(path.image_processed, path.processed)
    specialist = Beam()
    _, pred_labels, health_names = specialist.predict(data, names)
    save_classified(pred_labels, names, path)
    geometric = specialist.geometric(path, health_names)
    image_grid(data, pred_labels, path.plots)
    make_dataframe(pred_labels, path)

def remove_dataframe(path):
    if os.path.isfile(path.info + '/predicted.csv'):
        os.remove(path.info + '/predicted.csv')

def save_classified(pred_labels, names, path):
    for i in range(len(names)):
        img = cv2.imread('{0}/{1}.png'.format(path.image_processed, names[i]))
        cv2.imwrite('{0}/{1}/{2}.png'.format(path.image_classified, pred_labels[i], names[i]), img)

def make_dataframe(labels, path):
    df = pd.DataFrame()
    df['result'] = labels
    df['quantity'] = 1
    data = df.groupby(['result'], as_index=False).sum()
    data.to_csv('{}/{}'.format(path.info, 'predicted.csv'), index=False)

if __name__ == '__main__':
    client_id, analysis_id, = 0, 169
    main(client_id, analysis_id)
