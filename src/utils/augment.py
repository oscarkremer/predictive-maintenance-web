import sys
import os
import Augmentor

def augmentation(folder, label, number_samples):
    p = Augmentor.Pipeline(source_directory=folder, save_format="jpg")
    p.flip_left_right(0.5)
    p.flip_top_bottom(0.5)
    p.rotate(probability=0.3, max_left_rotation=10, max_right_rotation=10)
    p.sample(number_samples, multi_threaded=False)
    for index, filename in enumerate(os.listdir(folder + '/output')):
        dst = '{0}.{1}.jpg'.format(label, str(index+1))
        src = '{0}/output/{1}'.format(folder, filename)
        dst = '{0}/output/{1}'.format(folder, dst)
        os.rename(src, dst)
