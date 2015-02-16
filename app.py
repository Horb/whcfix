from flask import Flask, render_template, request, url_for, g, abort, flash, redirect, session
import logging
from whcfix.data.applicationstrings import ApplicationStrings
from whcfix.logic.matches import Matches
from whcfix.logic.divisions import Divisions
from whcfix.ui.elements import LastResultDashboardItem, NextMatchDashboardItem, TodaysMatchesDashboardItem
import whcfix.settings as settings
import os

if __name__ == '__main__':
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_directory)

app = Flask(__name__,
            template_folder='whcfix/templates',
            static_folder='whcfix/static',
            static_url_path='/static')

app.config.update(dict(
    SECRET_KEY=settings.DEVELOPMENT_KEY,
))

from whcfix.data.database import Session, init_db, test_post
from whcfix.data.models import Post

@app.before_first_request
def before_request():
    init_db()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != settings.BLOG_USER 
                or request.form['password'] != settings.BLOG_PASSWORD):
            error = 'Invalid username or password!'
        else:
            session['logged_in'] = True
            flash('You were logged in!')
            return redirect(url_for('news'))
    return render_template('login.html', error=error)

@app.route("/news")
def news():
    try:
        posts = Session().query(Post).all()
        return render_template("news.html", posts=posts)
    except Exception:
        logging.exception("")
        return render_template("501.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You were logged out!")
    return redirect(url_for("news"))

@app.route("/news/new", methods=['POST'])
def add_news():
    if not session.get('logged_in'):
        abort(401)
    post = Post(title=request.form['title'], body=request.form['body'])
    s = Session()
    s.add(post)
    s.commit()
    flash("New entry was successfully posted!")
    return redirect(url_for('news'))

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
        # Only include dashboard items that have content to display.
        dashboard_items = [ di for di in dashboard_items
                            if di.listOfMatches ]

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
        matches = Matches().get_matches(
                lambda m: m.doesFeature(team)
                )
        divisions = Divisions().get_divisions(
                lambda d: d.doesFeatureTeam(team)
                )
        return render_template("teamDump.html", team=team,
                               matches=matches,
                               divisions=divisions)
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
