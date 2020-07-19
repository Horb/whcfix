from whcfix.logic.matches import Matches
from flask import render_template, request, Blueprint
import whcfix.ui.elements as elements
from whcfix.data.applicationstrings import ApplicationStrings
import whcfix.settings as settings
from flask import send_from_directory

base = Blueprint('base', __name__, template_folder='whcfix/templates')


@base.route('/')
def home():
    matches = Matches()
    teams = matches.teamNames("Wakefield")
    kwargs = request.args.to_dict()
    nextMatches = matches.getNextMatches(teams, **kwargs)
    lastResults = matches.getLastResults(teams, **kwargs)
    todaysMatches = matches.getTodaysMatches(teams, **kwargs)
    dashboard_items = [elements.LastResultDashboardItem(lastResults),
                       elements.NextMatchDashboardItem(nextMatches),
                       elements.TwitterFeedDashboardItem(),
                       elements.TodaysMatchesDashboardItem(todaysMatches)]
    # Only include dashboard items that have content to display.
    dashboard_items = [di for di in dashboard_items if di.has_content()]
    return render_template("dashboard.html", strings=ApplicationStrings(),
                           dashboard_items=dashboard_items)


@base.route("/about/")
def about():
    return render_template("about.html")
