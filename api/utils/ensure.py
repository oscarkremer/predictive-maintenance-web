from contextlib import contextmanager


@contextmanager
def ensure_model_fitting():
    try:
        yield
    except Exception as e:
        pass
