import os
import sys
import numpy as np
from src.utils import full_process, log, log_time, path_helper


def main(image_path, processed_path):
    full_process(image_path, processed_path)


if __name__ == '__main__':
    client_id = 0
    ids = list(range(2, 3))
    for analysis_id in ids:b                                                                                                                                                                                                                                                                                                                                                                                                
        path = '../../data/client/{0}/{1}'.format(client_id, analysis_id)
        image_path = '../../data/client/{0}/{1}/images/raw/image.jpg'.format(
            client_id, analysis_id)
        image_path = os.path.join(os.path.dirname(__file__), image_path)
        processed_path = '../../data/client/{0}/{1}/images/processed'.format(
            client_id, analysis_id)
        processed_path = os.path.join(
            os.path.dirname(__file__), processed_path)
        processed_path = path_helper(processed_path)
        main(image_path, processed_path)
