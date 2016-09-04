import logging
from flask import Flask, render_template
from whcfix.fixtures import fixtures
from whcfix.base import base
import whcfix.settings as settings
import os

app = Flask(__name__, template_folder='whcfix/templates',
            static_folder='whcfix/static', static_url_path='/static')
app.secret_key = settings.DEVELOPMENT_KEY
app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER


@app.errorhandler(Exception)
def handle_exception(err):
    logging.exception("")
    return render_template("501.html")

app.register_blueprint(base)
app.register_blueprint(fixtures)


if __name__ == '__main__':
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_directory)
    logging.basicConfig(level=logging.DEBUG)
    app.debug = True
    app.run()
else:
    logging.basicConfig(level=logging.INFO)
