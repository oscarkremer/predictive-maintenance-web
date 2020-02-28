import os
import numpy as np
from src.specialist import Beam
from src.utils import Path
from src.utils.image_process import remove_emptyness

if __name__ == '__main__':
    path = Path(0, 185)
    beam = Beam()
    healths = []
    empty_number = remove_emptyness(path)
    for filename in os.listdir(path.image_processed):
        healths.append(filename.split('.')[0])
    df = beam.geometric(path, healths)
    