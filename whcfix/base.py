from whcfix.logic.matches import Matches
from flask import render_template, request, Blueprint
from whcfix.data.database import get_db
from whcfix.data.models import Post
import whcfix.ui.elements as elements
from whcfix.data.applicationstrings import ApplicationStrings
import whcfix.settings as settings
from flask import url_for, flash, redirect, session, send_from_directory

base = Blueprint('base', __name__, template_folder='whcfix/templates')


@base.route('/')
def home():
    with get_db() as db:
        matches = Matches()
        teams = matches.teamNames("Wakefield")
        kwargs = request.args.to_dict()
        posts = db.query(Post).filter(Post.is_published == True)
        posts = posts.order_by(Post.first_published_date).all()[::-1]
        nextMatches = matches.getNextMatches(teams, **kwargs)
        lastResults = matches.getLastResults(teams, **kwargs)
        todaysMatches = matches.getTodaysMatches(teams, **kwargs)
        dashboard_items = [elements.LastResultDashboardItem(lastResults),
                           elements.NextMatchDashboardItem(nextMatches),
                           elements.NewsPostsDashboardItem(posts),
                           elements.TwitterFeedDashboardItem(),
                           elements.TodaysMatchesDashboardItem(todaysMatches)]
        # Only include dashboard items that have content to display.
        dashboard_items = [di for di in dashboard_items if di.has_content()]
        return render_template("dashboard.html", strings=ApplicationStrings(),
                               dashboard_items=dashboard_items)


@base.route("/about/")
def about():
    return render_template("about.html")


@base.route('/uploads/<filename>/')
def uploads(filename):
    return send_from_directory(settings.UPLOAD_FOLDER, filename)


@base.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != settings.BLOG_USER
                or request.form['password'] != settings.BLOG_PASSWORD):
            error = 'Invalid username or password!'
        else:
            session['logged_in'] = True
            flash('You were logged in!')
            return redirect(url_for('news.news_home'))
    return render_template('login.html', error=error)


@base.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash("You were logged out!")
    return redirect(url_for("base.home"))
