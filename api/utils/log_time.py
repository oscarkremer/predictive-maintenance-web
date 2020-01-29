from contextlib import contextmanager
from datetime import timedelta
from .logger import log
import time


@contextmanager
def log_time(title):
    start = time.time()
    log('Started ' + title)
    try:
        yield
    finally:
        log('Done ' + title + ' in ' + str(timedelta(seconds=time.time() - start)))


    