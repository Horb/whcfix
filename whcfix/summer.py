from flask import render_template, Blueprint
from whcfix.data.database import get_db
from whcfix.data.models import Division, Fixture, Result
import logging

summer = Blueprint('summer', __name__, template_folder='whcfix/templates')

@summer.route("/summer/")
def home():
    logging.info("enter teams")
    with get_db() as db:
        divisions = db.query(Division).all()
        for d in divisions:
            for t in d.teams:
                decorate_points(t)
        fixtures = db.query(Fixture).all()
        results = db.query(Result).all()
        return render_template("summer.html", 
                divisions=divisions,
                fixtures=fixtures,
                results=results)

def decorate_points(team):
    team.won = 0
    team.lost = 0
    team.drawn = 0
    team.goal_difference = 0
    for f in team.home_fixtures:
        result = f.result
        if len(result) > 0:
            result = result[0]
            team.goal_difference += result.home_goals - result.away_goals
            if result.home_goals > result.away_goals:
                team.won += 1
            if result.home_goals < result.away_goals:
                team.lost += 1
            if result.home_goals == result.away_goals:
                team.drawn += 1
    for f in team.away_fixtures:
        result = f.result
        if len(result) > 0:
            result = result[0]
            team.goal_difference += result.away_goals - result.home_goals
            if result.away_goals > result.home_goals:
                team.won += 1
            if result.away_goals < result.home_goals:
                team.lost += 1
            if result.away_goals == result.home_goals:
                team.drawn += 1
    team.points = 3 * team.won + 1 * team.drawn
