from flask import Flask, render_template
import logic

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route("/")
def hello():
    matches = logic.getMatchesObject()
    teams = matches.listOfTeamNames(searchTerm="Wakefield")
    return render_template("dashboard.html"
                           , strings = logic.appStrings()
                           , recent_form = matches.recentForm(teams)
                           , nextMatches = matches.getNextMatches(teams)
                           , lastResults = matches.getLastResults(teams)
                           )

@app.route("/teams/<team>/")
def team(team):
    matches = logic.getMatchesObject()
    return render_template("teamDump.html", team = team, matches = matches.getMatches(team))

@app.route("/teams/")
def teams():
    matches = logic.getMatchesObject()
    return render_template("teamDump.html", matches = matches.listOfMatches)

if __name__ == '__main__':
    app.debug = True
    app.run()
