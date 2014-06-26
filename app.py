from flask import Flask, render_template
from whcfix.data.ApplicationStrings import ApplicationStrings
import whcfix.logic.models as models
import os

if __name__ == '__main__':
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_directory)

app = Flask(__name__,
            template_folder='whcfix/templates',
            static_folder='whcfix/static',
            static_url_path='/static')


@app.route("/")
def maintenance():
    return render_template("maintenance.html", strings=ApplicationStrings())

@app.route("/teams/")
def teams():
    matches = models.Matches()
    teams = matches.teamNames("Wakefield")
    return render_template("teams.html", teams=teams,
                           strings=ApplicationStrings())


# @app.route("/")
# def hello():
#     matches = models.Matches()
#     teams = matches.teamNames("Wakefield")
#     return render_template("dashboard.html"
#                           , strings = logic.appStrings()
#                           , recent_form = matches.recentForm(teams)
#                           , nextMatches = matches.getNextMatches(teams)
#                           , lastResults = matches.getLastResults(teams)
#                            )
# @app.route("/recent_form/")
# def recent_form():
#     matches = models.Matches()
#     teams = matches.teamNames("Wakefield")
#     return render_template("recent_form.html"
#                           , recent_form = matches.recentForm(teams)
#                            )

# @app.route("/last_result/")
# def last_result():
#     matches = models.Matches()
#     teams = matches.teamNames("Wakefield")
#     return render_template("last_result.html"
#                           , lastResults = matches.getLastResults(teams)
#                            )

# @app.route("/next_match/")
# def next_match():
#     matches = models.Matches()
#     teams = matches.teamNames("Wakefield")
#     return render_template("next_match.html"
#                           , nextMatches = matches.getNextMatches(teams)
#                            )

# @app.route("/teams/<team>/")
# def team(team):
#     matches = models.Matches()
#     return render_template("teamDump.html",
#                            team = team, matches = matches.teamFilter(team))

# @app.route("/teams/")
# def teams():
#     matches = models.Matches()
#     return render_template("teamDump.html",
#                            team = "All", matches = matches.listOfMatches)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0')
