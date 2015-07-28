from whcfix.logic.matches import Matches
from whcfix.logic.divisions import Divisions
from flask import render_template, request, Blueprint
from whcfix.data.database import get_db
from whcfix.data.models import match_reports_for
from whcfix.data.applicationstrings import ApplicationStrings

fixtures = Blueprint('fixtures', __name__, template_folder='whcfix/templates')


@fixtures.route("/teams/", methods=['GET'])
def teams():
    matches = Matches()
    teams = matches.teamNames("Wakefield", **request.args.to_dict())
    return render_template("teams.html",
                           teams=teams,
                           strings=ApplicationStrings())


@fixtures.route("/teams/<team>/")
def team(team):
    with get_db() as db:
        match_reports = match_reports_for(team, db)
        matches = Matches().get_matches(lambda m: m.doesFeature(team))
        d_cond = lambda d: d.doesFeatureTeam(team)
        divisions = Divisions().get_divisions(d_cond)
        return render_template("teamDump.html", team=team,
                               matches=matches,
                               divisions=divisions,
                               match_reports=match_reports)


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
