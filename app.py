from flask import Flask, render_template, request, url_for, g, abort, flash, redirect, session, send_from_directory
from werkzeug import secure_filename
import datetime
import logging
from whcfix.data.applicationstrings import ApplicationStrings
from whcfix.logic.matches import Matches
from whcfix.logic.divisions import Divisions
from whcfix.ui.elements import LastResultDashboardItem, NextMatchDashboardItem, TodaysMatchesDashboardItem, NewsPostsDashboardItem, TwitterFeedDashboardItem
import whcfix.settings as settings
import os

if __name__ == '__main__':
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_directory)

app = Flask(__name__,
            template_folder='whcfix/templates',
            static_folder='whcfix/static',
            static_url_path='/static')

app.secret_key = settings.DEVELOPMENT_KEY

app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER

from whcfix.data.database import init_db, get_db
from whcfix.data.models import Post, MatchReport, match_reports_for

@app.errorhandler(Exception)
def handle_exception(err):
    logging.exception("")
    return render_template("501.html")

@app.before_first_request
def before_first_request():
    init_db()

@app.route('/uploads/<filename>/')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/select_match_for_match_report/<team>/")
def select_match_for_match_report(team):
    matches = Matches().get_matches(lambda m: m.doesFeature(team))
    return render_template('select_match_for_match_report.html', 
                           matches=matches,
                           team=team)

@app.route('/submit_match_report/<home>/<away>/<date>/<time>/', methods=['GET', 'POST'])
def submit_match_report(home, away, date, time):
    if request.method == 'POST':
        title = "Match Report: %s vs %s" % (home, away)
        body = request.form['body']
        image_file_name = save_image_from_form(request.form, 'image')
        match_report = MatchReport()
        match_report.is_published = False
        match_report.title = title
        match_report.home = home
        match_report.away = away
        match_report.push_back = datetime.datetime.strptime("%s %s" % (date, time),
                                                            "%d-%m-%y %H:%M")
        match_report.body = body
        match_report.image_file_name = image_file_name
        with get_db() as db:
            db.add(match_report)
        flash("Thank you for your submission.")
        return redirect(url_for('home'))
    else: 
        return render_template("submit_match_report.html", 
                               home=home, 
                               away=away, 
                               date=date,
                               time=time) 

@app.route('/news/post/<int:post_id>/', methods=['GET', 'POST'])
def post_detail(post_id):
    with get_db() as db:
        post = db.query(Post).filter(Post.id == post_id).first()
        if post:
            logging.debug("Found post with id=%s" % post.id)
            if request.method == 'POST':
                logging.debug("POST recieved")
                post.title = request.form['title']
                post.body = request.form['body']
                post.is_published = 'published' in request.form
                if 'published' in request.form:
                    post.publish()
                post.image_file_name = save_image_from_form(request.form, 'image')
                flash("Successfully Saved!")
                return redirect(url_for('post_detail', post_id=post.id))
            else:
                logging.debug("GET recieved")
                return render_template('post_detail.html', post=post)
        else:
            abort(404)

@app.route('/login/', methods=['GET', 'POST'])
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

@app.route("/delete_post/<int:post_id>/")
def delete_post(post_id):
    kwargs = request.args.to_dict()
    with get_db() as db:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not session['logged_in']:
            abort(401)
        elif not post:
            abort(404)
        elif not kwargs.has_key('confirmed'):
            message = "You're about to delete the post: %s. Are you sure?" % (post.title,)
            action_message = "Delete Post."
            return render_template('confirm.html', 
                                   message=message, 
                                   action_message=action_message,
                                   post=post)
        else:
            db.delete(post)
            flash("Post deleted.")
            return redirect(url_for("news"))

def lookup_and_do(Model, id, action, redirect_url, redirect_parameters):
    if not session['logged_in']:
        abort(401)
    else:
        with get_db() as db:
            instance = db.query(Model).filter(Model.id == id).first()
            if instance:
                action(instance)
                return redirect(url_for(redirect_url, **redirect_parameters))
            else:
                abort(404)

@app.route("/unpublish_post/<int:post_id>/")
def unpublish_post(post_id):
    return lookup_and_do(Post, post_id, 
                         lambda p: p.unpublish(), 
                         'news', { 'post_id': post_id})

@app.route("/publish_post/<int:post_id>/")
def publish_post(post_id):
    return lookup_and_do(Post, post_id,
                         lambda p: p.publish(),
                         'news', { 'post_id' : post_id})

@app.route("/news/")
def news():
    with get_db() as db:
        posts = db.query(Post).order_by(Post.first_published_date, Post.id).all()[::-1]
        return render_template("news.html", posts=posts)

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash("You were logged out!")
    return redirect(url_for("home"))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in settings.ALLOWED_UPLOAD_EXTENSIONS

def save_image_from_form(form, image_field):
    file = request.files[image_field]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_file_path)
        return filename
    else:
        return None

@app.route("/news/new/", methods=['POST'])
def add_news():
    post = Post()
    post.title=request.form['title']
    post.body=request.form['body']
    post.is_published='published' in request.form
    if 'published' in request.form:
        post.publish()
    post.image_file_name = save_image_from_form(request.form, 'image')
    with get_db() as db:
        db.add(post)
    flash("New entry was successfully posted!")
    return redirect(url_for('news'))

@app.route("/")
def home():
    with get_db() as db:
        matches = Matches()
        teams = matches.teamNames("Wakefield")
        kwargs = request.args.to_dict()
        posts = db.query(Post).filter(Post.is_published==True).order_by(Post.first_published_date).all()[::-1]
        nextMatches = matches.getNextMatches(teams, **kwargs)
        lastResults = matches.getLastResults(teams, **kwargs)
        todaysMatches = matches.getTodaysMatches(teams, **kwargs)
        dashboard_items = [LastResultDashboardItem(lastResults), 
                           NextMatchDashboardItem(nextMatches), 
                           NewsPostsDashboardItem(posts), 
                           TwitterFeedDashboardItem(), 
                           TodaysMatchesDashboardItem(todaysMatches)]
        # Only include dashboard items that have content to display.
        dashboard_items = [ di for di in dashboard_items if di.has_content() ]
        return render_template("dashboard.html",
                               strings=ApplicationStrings(),
                               dashboard_items=dashboard_items)

@app.route("/teams/", methods=['GET',])
def teams():
    matches = Matches()
    teams = matches.teamNames("Wakefield", **request.args.to_dict())
    return render_template("teams.html",
                           teams=teams,
                           strings=ApplicationStrings())

@app.route("/teams/<team>/")
def team(team):
    with get_db() as db:
        match_reports = match_reports_for(team, db)
        matches = Matches().get_matches(
                lambda m: m.doesFeature(team)
                )
        divisions = Divisions().get_divisions(
                lambda d: d.doesFeatureTeam(team)
                )
        return render_template("teamDump.html", team=team,
                               matches=matches,
                               divisions=divisions,
                               match_reports=match_reports)

@app.route("/teams/<team>/compact/")
def teamBrief(team):
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

@app.route("/next_match/", methods=['GET',])
def next_match():
    matches = Matches()
    teams = matches.teamNames("Wakefield")
    nextMatches = matches.getNextMatches(teams, **request.args.to_dict())
    return render_template("next_match.html", nextMatches=nextMatches)

@app.route("/last_result/", methods=['GET',])
def last_result():
    matches = Matches()
    teams = matches.teamNames("Wakefield")
    lastResults = matches.getLastResults(teams, **request.args.to_dict())
    return render_template("last_result.html", lastResults=lastResults)

@app.route("/recent_form/", methods=['GET',])
def recent_form():
    matches = Matches()
    teams = matches.teamNames("Wakefield")
    recent_form = matches.recentForm(teams, **request.args.to_dict())
    return render_template("recent_form.html", recent_form=recent_form)

@app.route("/about/")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.debug = True
    app.run()
else:
    logging.basicConfig(level=logging.INFO)
