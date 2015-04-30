import logging
import csv
from flask import Flask, render_template
from whcfix.data.database import init_db
from whcfix.fixtures import fixtures
from whcfix.base import base
from whcfix.news import news
from whcfix.tournament import tournaments
import whcfix.settings as settings
from whcfix.logic.match import Match
from datetime import datetime, time
import os

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
app.register_blueprint(tournaments, url_prefix='/tournaments')

def icsv(fn):
    with open(fn, 'r') as csvf:
        reader = csv.reader(csvf)
        for line in reader:
            yield line

def line_to_match(line):
    logging.debug(line)
    y, m, d, h, n, s, venue, home, away = line
    y, m, d, h, n, s = map(int, [y, m, d, h, n, s])
    return Match(datetime(y, m, d), time(h, n, s), venue, home, None, None, away, False, "")

@app.route('/summer_league/')
def summer_league():
    matches = list(map(line_to_match, icsv('whcfix/summerleaguefixtures1.csv')))
    return render_template('static_summer_league.html', matches=matches)

if __name__ == '__main__':
    import os
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_directory)
    logging.basicConfig(level=logging.DEBUG)
    app.debug = True
    app.run()
else:
    logging.basicConfig(level=logging.INFO)
