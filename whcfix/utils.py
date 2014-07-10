import logging

def log_exceptions(func):
    def _log_exceptions(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            logging.exception("args: %s, kwargs %s" % (args, kwargs))
            raise
    return _log_exceptions

def nz(func):
    def _nz(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            return ""
        else:
            return result
    return _nz

import pprint

class PrettyLog(object):

    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return pprint.pformat(self.obj)
