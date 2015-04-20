from flask import Flask, render_template, request, url_for, g, abort, flash, redirect, session, send_from_directory
import datetime
import logging
from whcfix.data.applicationstrings import ApplicationStrings
from whcfix.data.database import init_db, get_db
from whcfix.data.models import Post, MatchReport, match_reports_for
from whcfix.logic.matches import Matches
from whcfix.logic.divisions import Divisions
from whcfix.ui.elements import LastResultDashboardItem, NextMatchDashboardItem, TodaysMatchesDashboardItem, NewsPostsDashboardItem, TwitterFeedDashboardItem
import whcfix.settings as settings
from whcfix.utils import lookup_and_do, save_image_from_form
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

if __name__ == '__main__':
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_directory)
    logging.basicConfig(level=logging.DEBUG)
    app.debug = True
    app.run()
else:
    logging.basicConfig(level=logging.INFO)
