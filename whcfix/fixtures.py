from whcfix.logic.matches import Matches
from whcfix.logic.divisions import Divisions
from flask import render_template, request, Blueprint, Response
from whcfix.data.applicationstrings import ApplicationStrings
from itertools import groupby
from collections import OrderedDict
from datetime import datetime, time, timedelta
from ics import Calendar, Event
from md5 import md5

fixtures = Blueprint('fixtures', __name__, template_folder='whcfix/templates')


@fixtures.route("/teams/")
def teams():
    matches = Matches()
    teams = matches.teamNames("Wakefield", **request.args.to_dict())
    # TODO Remove this hack
    teams = filter(lambda t: "Wanderers" not in t, teams)
    return render_template("teams.html",
                           teams=teams,
                           strings=ApplicationStrings())

@fixtures.route("/fixtures/by_date/")
def fixtures_by_date():
    matches = Matches()
    teams = matches.teamNames("Wakefield", **request.args.to_dict())
    matches = matches.get_matches(lambda m: m.home in teams or m.away in teams)
    matches.sort()
    # First date in the future
    dates = { m._date for m in matches }
    dates_in_the_future = { d for d in dates if d > datetime.now() }
    if dates_in_the_future:
        scroll_to_date = min(dates_in_the_future)
    else:
        scroll_to_date = min(dates)
    return render_template("fixtures_by_date.html",
                           matches = matches,
                           scroll_to_date = scroll_to_date)

def fixture_uid(m):
    content = "%s vs %s %s%s%s" % (m.home, m.away, m._date.year, m._date.month, m._date.day)
    hexdigest = md5(content).hexdigest()
    return "%s@whcfix.com" % (hexdigest)

@fixtures.route("/teams/<team>/calendar.ics")
def team_ics(team):
    matches = Matches().get_matches(lambda m: m.doesFeature(team))
    c = Calendar()
    for m in matches:
        if not m._date:
            continue

        e = Event(uid=fixture_uid(m), location=m.venue)
        e.name = "%s vs %s" % (m.home, m.away)


        if not m._time:
            m._time = time(0,0,0)

        begin = datetime(m._date.year,
                         m._date.month,
                         m._date.day,
                         m._time.hour,
                         m._time.minute,
                         m._time.second)
        e.begin = begin
        e.duration = timedelta(minutes=90)
        c.events.append(e)
    return Response(c, mimetype='text/calendar')

@fixtures.route("/fixtures/by_team/")
def fixtures_by_team():
    matches = Matches()
    teams = matches.teamNames("Wakefield", **request.args.to_dict())
    matches_by_team = OrderedDict()
    for team in teams:
        team_matches = matches.get_matches(lambda m: m.doesFeature(team))
        team_matches.sort()
        matches_by_team[team] = team_matches
    return render_template("fixtures_by_team.html",
                           matches_by_team = matches_by_team)


@fixtures.route("/teams/<team>/")
def team(team):
    matches = Matches().get_matches(lambda m: m.doesFeature(team))
    d_cond = lambda d: d.doesFeatureTeam(team)
    divisions = Divisions().get_divisions(d_cond)
    return render_template("teamDump.html", team=team,
                           matches=matches,
                           divisions=divisions)


@fixtures.route("/teams/<team>/compact/")
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

    divisions = d.get_divisions(lambda d: d.doesFeatureTeam(team))
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


@fixtures.route("/next_match/", methods=['GET'])
def next_match():
    matches = Matches()
    teams = matches.teamNames("Wakefield")
    nextMatches = matches.getNextMatches(teams, **request.args.to_dict())
    return render_template("next_match.html", nextMatches=nextMatches)


@fixtures.route("/last_result/", methods=['GET'])
def last_result():
    matches = Matches()
    teams = matches.teamNames("Wakefield")
    lastResults = matches.getLastResults(teams, **request.args.to_dict())
    return render_template("last_result.html", lastResults=lastResults)


@fixtures.route("/recent_form/", methods=['GET'])
def recent_form():
    matches = Matches()
    teams = matches.teamNames("Wakefield")
    recent_form = matches.recentForm(teams, **request.args.to_dict())
    return render_template("recent_form.html", recent_form=recent_form)
