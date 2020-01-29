import logging
import sys
import os

logging.getLogger('fbprophet').setLevel(logging.WARNING)


class Logger(object):
    def __init__(self, log_file='data/logs/output.log'):
        self.log_file = os.path.abspath(log_file)
        self.console = logging.StreamHandler(sys.stdout)
        self.console.setLevel(logging.INFO)
        self.formatter = logging.Formatter('---> %(message)s')
        self.console.setFormatter(self.formatter)
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=self.log_file,
            filemode='a')

    def log(self, lvl, msg):
        if 'LOGGER' in os.environ and os.environ['LOGGER'] == 'stdout':
            logging.getLogger('').addHandler(self.console)

        logging.log(lvl, msg)


logger = Logger()


def log(msg, lvl=logging.INFO):
    logger.log(lvl, msg)
