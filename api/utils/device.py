import torch
from distutils.version import LooseVersion

class Device(dict):
    def __init__(self):
        self['xgboost'] = "auto"
        self['lstm'] = torch.device('cpu')
        if torch.cuda.is_available():
            self['lstm'] = torch.device('cuda')

processing_device = Device()
