from flask import render_template, Blueprint
from whcfix.data.database import get_db
from whcfix.data.models import Division
import logging

summer = Blueprint('summer', __name__, template_folder='whcfix/templates')

@summer.route("/summer/")
def home():
    return 'Hello World <a href="teams/">Teams</a> '

@summer.route("/summer/teams/")
def teams():
    logging.info("enter teams")
    with get_db() as db:
        divisions = db.query(Division).all()
        return render_template("summer_teams.html", divisions=divisions)

@summer.route("/summer/teams/<team_name>/")
def team(team_name):
    with get_db() as db:
        team=None
        return render_template("team.html")
