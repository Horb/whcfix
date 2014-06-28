import logging

def log_exceptions(func):
    def _log_exceptions(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            logging.exception("args: %s, kwargs %s" % (args, kwargs))
            raise
    return _log_exceptions
