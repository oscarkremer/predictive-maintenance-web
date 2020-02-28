import os

LABELS = ['saudavel', 'caruncho', 'ardido&mofado', 'manchado', 'mordido', 'bandinha', 
            'contaminantes', 'genetico']

class Path:
    def __init__(self, client_id=0, analysis_id=0):
        self.path = '../../data/client/{0}/{1}'.format(client_id, analysis_id)
        self.image_raw = os.path.join(os.path.dirname(
            __file__), '{0}/{1}'.format(self.path, 'images/raw'))
        self.white_raw = os.path.join(os.path.dirname(
            __file__), '{0}/{1}'.format(self.path, 'images/raw/white'))
        self.blue_raw = os.path.join(os.path.dirname(
            __file__), '{0}/{1}'.format(self.path, 'images/raw/blue'))
        self.image_processed = os.path.join(os.path.dirname(
            __file__), '{0}/{1}'.format(self.path, 'images/processed'))
        self.image_classified = os.path.join(os.path.dirname(
            __file__), '{0}/{1}'.format(self.path, 'images/classified'))
        self.info = os.path.join(os.path.dirname(
            __file__), '{0}/{1}'.format(self.path, 'info'))
        self.processed = os.path.join(os.path.dirname(
            __file__), '{0}/{1}'.format(self.path, 'processed'))
        self.plots = os.path.join(os.path.dirname(
            __file__), '{0}/{1}'.format(self.path, 'plots'))
        self.report = os.path.join(os.path.dirname(
            __file__), '{0}/{1}'.format(self.path, 'report'))
        self.check()

    def check(self):
        path_helper(self.path)
        path_helper(self.image_raw)
        path_helper(self.white_raw)
        path_helper(self.blue_raw)
        path_helper(self.image_processed)
        path_helper(self.image_classified)
        for label in LABELS:
            path_helper('{0}/{1}'.format(self.image_classified, label))
        path_helper(self.info)
        path_helper(self.processed)
        path_helper(self.plots)
        path_helper(self.report)

def path_helper(path):
    try:
        os.makedirs(path)
    except OSError:
        pass
    return path
