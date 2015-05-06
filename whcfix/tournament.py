import logging
from flask import Blueprint, render_template, request, abort, url_for, redirect
from whcfix.data.models import Team, Division, Tournament
from whcfix.data.database import get_db
from functools import wraps

tournaments = Blueprint('tournaments', __name__, template_folder='whcfix/templates')

@tournaments.route('/')
def tournament_home():
    ''' A list of the active tournaments. '''
    with get_db() as db:
        tournaments = db.query(Tournament).all()
        return render_template('tournaments/main.html', tournaments=tournaments)

@tournaments.route('/tournaments/<int:tournament_id>/')
def tournament_detail(tournament_id):
    ''' A list of the active tournaments. '''
    with get_db() as db:
        t = db.query(Tournament).filter(Tournament.id==tournament_id).first()
        return render_template('tournaments/dashboard.html', tournament=t)

@tournaments.route('/division/<int:division_id>/')
def division_home(division_id):
    ''' Render a dashboard for the division. '''

@tournaments.route('/log_result/')
def log_result():
    ''' Serve or parse a form to log results. '''

@tournaments.route('/team/<int:team_id>/')
def team_home(team_id):
    ''' Render a dashboard for the team. '''

def serve_or_parse_form(template_name, get_object_from_form, redirect_url, **kwargs):
    ''' Serve or parse a form. '''
    logging.debug("%s %s %s" % (template_name, get_object_from_form, redirect_url))
    if request.method == 'GET':
        return render_template(template_name, **kwargs)
    elif request.method == 'POST':
        with get_db() as db:
            form = request.form
            db.add(get_object_from_form(form))
            return redirect(redirect_url)
    else:
        abort(405)

@tournaments.route('/division/new/<int:tournament_id>/', methods=['GET', 'POST'])
def division_new(tournament_id):
    ''' Serve or parse a form to add a division. '''
    return serve_or_parse_form('tournaments/forms/division_new.html',
                               lambda f: Division(name=f['name'], tournament_id=tournament_id),
                               url_for('tournaments.admin'),
                               tournament_id=tournament_id)

@tournaments.route('/team/new/<int:division_id>/', methods=['GET', 'POST'])
def team_new(division_id):
    ''' Serve or parse a form to add a team. '''
    return serve_or_parse_form('tournaments/forms/team_new.html',
                               lambda f: Team(name=f['name'], division_id=division_id),
                               url_for('tournaments.admin'),
                               division_id=division_id)

@tournaments.route('/tournament/new/', methods=['GET', 'POST'])
def tournament_new():
    ''' Serve or parse a form to add a tournament. '''
    return serve_or_parse_form('tournaments/forms/tournament_new.html',
                               lambda f: Tournament(name=f['name']),
                               url_for('tournaments.admin'))

@tournaments.route('/admin/')
def admin():
    ''' A list of all objects and links to create objects. '''
    with get_db() as db:
        tournament_list = db.query(Tournament).all()
        return render_template('tournaments/admin.html', tournaments = tournament_list)

