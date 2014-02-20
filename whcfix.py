from flask import Flask, render_template
import logic
import models
import os
os.chdir('/var/www/whcfix')

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route("/")
def hello():
    matches = models.Matches()
    teams = matches.teamNames("Wakefield")
    return render_template("dashboard.html"
                           , strings = logic.appStrings()
                           , recent_form = matches.recentForm(teams)
                           , nextMatches = matches.getNextMatches(teams)
                           , lastResults = matches.getLastResults(teams)
                           )

@app.route("/teams/<team>/")
def team(team):
    matches = models.Matches()
    return render_template("teamDump.html", team = team, matches = matches.teamFilter(team))

@app.route("/teams/")
def teams():
    matches = models.Matches()
    return render_template("teamDump.html", team = "All", matches = matches.listOfMatches)

if __name__ == '__main__':
    app.debug = True
    app.run()
