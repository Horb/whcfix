import logging
from flask import Flask, render_template
from whcfix.data.database import init_db
from whcfix.fixtures import fixtures
from whcfix.base import base
from whcfix.news import news
import whcfix.settings as settings


app = Flask(__name__, template_folder='whcfix/templates',
            static_folder='whcfix/static', static_url_path='/static')
app.secret_key = settings.DEVELOPMENT_KEY
app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER

@app.errorhandler(Exception)
def handle_exception(err):
    logging.exception("")
    return render_template("501.html")

@app.before_first_request
def before_first_request():
    init_db()

app.register_blueprint(base)
app.register_blueprint(fixtures)
app.register_blueprint(news)

if __name__ == '__main__':
    import os
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_directory)
    logging.basicConfig(level=logging.DEBUG)
    app.debug = True
    app.run()
else:
    logging.basicConfig(level=logging.INFO)
