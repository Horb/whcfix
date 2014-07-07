from flask import Flask, render_template
import logging
from whcfix.data.applicationstrings import ApplicationStrings
from whcfix.logic.matches import Matches
import os

if __name__ == '__main__':
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_directory)

app = Flask(__name__,
            template_folder='whcfix/templates',
            static_folder='whcfix/static',
            static_url_path='/static')


# @app.route("/maintenance")
# def maintenance():
#     try:
#         return render_template("maintenance.html",
#                                strings=ApplicationStrings())
#     except Exception:
#         logging.exception("")
#         return render_template("501.html")


@app.route("/teams/")
def teams():
    try:
        matches = Matches()
        teams = matches.teamNames("Wakefield")
        return render_template("teams.html",
                               teams=teams,
                               strings=ApplicationStrings())
    except Exception:
        logging.exception("")
        return render_template("501.html")


@app.route("/")
def hello():
    try:
        matches = Matches()
        teams = matches.teamNames("Wakefield")
        return render_template("dashboard.html",
                               strings=ApplicationStrings(),
                               recent_form=matches.recentForm(teams),
                               nextMatches=matches.getNextMatches(teams),
                               lastResults=matches.getLastResults(teams))
    except Exception:
        logging.exception("")
        return render_template("501.html")


@app.route("/recent_form/")
def recent_form():
    try:
        matches = Matches()
        teams = matches.teamNames("Wakefield")
        return render_template("recent_form.html",
                               recent_form=matches.recentForm(teams))
    except Exception:
        logging.exception("")
        return render_template("501.html")


@app.route("/last_result/")
def last_result():
    try:
        matches = Matches()
        teams = matches.teamNames("Wakefield")
        return render_template("last_result.html",
                               lastResults=matches.getLastResults(teams))
    except Exception:
        logging.exception("")
        return render_template("501.html")


@app.route("/next_match/")
def next_match():
    try:
        matches = Matches()
        teams = matches.teamNames("Wakefield")
        return render_template("next_match.html",
                               nextMatches=matches.getNextMatches(teams))
    except Exception:
        logging.exception("")
        return render_template("501.html")


@app.route("/teams/<team>/")
def team(team):
    try:
        m = Matches()
        return render_template("teamDump.html", team=team,
                               matches=m.get_matches(lambda m:
                                                     m.doesFeature(team)))
    except Exception:
        logging.exception("")
        return render_template("501.html")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.debug = True
    app.run('0.0.0.0')
else:
    logging.basicConfig(level=logging.INFO)
