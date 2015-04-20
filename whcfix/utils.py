import logging
from werkzeug import secure_filename
from flask import request

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in settings.ALLOWED_UPLOAD_EXTENSIONS

def save_image_from_form(form, image_field):
    file = request.files[image_field]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_file_path)
        return filename
    else:
        return None

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

def catch_log_return_None(func):
    def _catch_log_return_None(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logging.exception("args: %s, kwargs %s" % (args, kwargs))
            return None
    return _catch_log_return_None


class PrettyLog(object):

    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        import pprint
        return pprint.pformat(self.obj)
