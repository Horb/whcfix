from flask import Flask, render_template
import logic

app = Flask(__name__, static_folder='static', static_url_path='/static')
conf = logic.getConfig()


@app.route("/")
def hello():
    matches = logic.getMatchesObject(conf['LEAGUE_ID'][0], conf['LEAGUE_ID'][1], conf['CLUB_ID'])
    return render_template("dashboard.html"
                           , recent_form = matches.recentForm(conf['teams'])
                           , nextMatches = matches.getNextMatches(conf['teams'])
                           , lastResults = matches.getLastResults(conf['teams']))

@app.route("/team/<team>/")
def team(team):
    matches = logic.getMatchesObject(conf['LEAGUE_ID'][0], conf['LEAGUE_ID'][1], conf['CLUB_ID'])
    return render_template("teamDump.html", matches = matches.getMatches(team))

if __name__ == '__main__':
    app.run()
