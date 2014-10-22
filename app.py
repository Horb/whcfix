from flask import Flask, render_template, request
import logging
from whcfix.data.applicationstrings import ApplicationStrings
from whcfix.logic.matches import Matches
from whcfix.logic.divisions import Divisions
from whcfix.ui.elements import LastResultDashboardItem, NextMatchDashboardItem, TodaysMatchesDashboardItem
import os

if __name__ == '__main__':
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_directory)

app = Flask(__name__,
            template_folder='whcfix/templates',
            static_folder='whcfix/static',
            static_url_path='/static')


@app.route("/")
def home():
    try:
        matches = Matches()
        teams = matches.teamNames("Wakefield")
        kwargs = request.args.to_dict()
        nextMatches = matches.getNextMatches(teams, **kwargs)
        lastResults = matches.getLastResults(teams, **kwargs)
        todaysMatches = matches.getTodaysMatches(teams, **kwargs)
        dashboard_items = [LastResultDashboardItem(lastResults), 
                           NextMatchDashboardItem(nextMatches), 
                           TodaysMatchesDashboardItem(todaysMatches)]

        return render_template("dashboard.html",
                               strings=ApplicationStrings(),
                               dashboard_items=dashboard_items)
    except Exception:
        logging.exception("")
        return render_template("501.html")


@app.route("/teams/", methods=['GET',])
def teams():
    try:
        matches = Matches()
        teams = matches.teamNames("Wakefield", **request.args.to_dict())
        return render_template("teams.html",
                               teams=teams,
                               strings=ApplicationStrings())
    except Exception:
        logging.exception("")
        return render_template("501.html")


@app.route("/teams/<team>/")
def team(team):
    try:
        m = Matches()
        d = Divisions()
        return render_template("teamDump.html", team=team,
                               matches=m.get_matches(lambda m: m.doesFeature(team)),
                               divisions=d.get_divisions(lambda d: d.doesFeatureTeam(team)))
    except Exception:
        logging.exception("")
        return render_template("501.html")


@app.route("/teams/<team>/compact/")
def teamBrief(team):
    try:
        m = Matches()
        d = Divisions()
        matches = m.get_matches(lambda m: m.doesFeature(team))

        last_result = m.lastResult(team)
        if last_result:
            last_result_index = matches.index(last_result)
            matches = [match for n, match in enumerate(matches) 
                       if abs(last_result_index - n) <= 2]
        else:
            matches = matches[:5]

        divisions=d.get_divisions(lambda d: d.doesFeatureTeam(team))
        if len(divisions) == 1:
            division = divisions[0]
            row_of_interest = None
            for n, row in enumerate(division.rows):
                if row.team == team:
                    row_of_interest = n
            if row_of_interest is not None:
                division.rows = [row for n, row in enumerate(division.rows) 
                                 if abs(row_of_interest - n) <= 2]

        return render_template("teamDump.html", 
                               team=team,
                               matches=matches,
                               divisions=divisions)
    except Exception:
        logging.exception("")
        return render_template("501.html")


@app.route("/next_match/", methods=['GET',])
def next_match():
    try:
        matches = Matches()
        teams = matches.teamNames("Wakefield")
        nextMatches = matches.getNextMatches(teams, **request.args.to_dict())
        return render_template("next_match.html", nextMatches=nextMatches)
    except Exception:
        logging.exception("")
        return render_template("501.html")


@app.route("/last_result/", methods=['GET',])
def last_result():
    try:
        matches = Matches()
        teams = matches.teamNames("Wakefield")
        lastResults = matches.getLastResults(teams, **request.args.to_dict())
        return render_template("last_result.html", lastResults=lastResults)
    except Exception:
        logging.exception("")
        return render_template("501.html")


@app.route("/recent_form/", methods=['GET',])
def recent_form():
    try:
        matches = Matches()
        teams = matches.teamNames("Wakefield")
        recent_form = matches.recentForm(teams, **request.args.to_dict())
        return render_template("recent_form.html", recent_form=recent_form)
    except Exception:
        logging.exception("")
        return render_template("501.html")


@app.route("/about/")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.debug = True
    app.run()
else:
    logging.basicConfig(level=logging.INFO)
