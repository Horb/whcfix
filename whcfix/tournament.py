from flask import Blueprint, render_template, request, abort, url_for, redirect
from whcfix.data.models import Team, Division, Tournament
from whcfix.data.database import get_db
from functools import wraps

tournaments = Blueprint('tournaments', __name__, template_folder='whcfix/templates')

@tournaments.route('/')
def tournament_home():
    ''' A list of the active tournaments. '''
    return ''' A list of the active tournaments. '''

@tournaments.route('/division/<int:division_id>/')
def division_home(division_id):
    ''' Render a dashboard for the division. '''

@tournaments.route('/log_result/')
def log_result():
    ''' Serve or parse a form to log results. '''

@tournaments.route('/team/<int:team_id>/')
def team_home(team_id):
    ''' Render a dashboard for the team. '''

@tournaments.route('/team/new/', methods=['GET', 'POST'])
def team_new():
    ''' Serve or parse a form to add a team. '''
    return ''' Serve or parse a form to add a team. '''

def serve_or_parse_form(template_name, get_object_from_form, redirect_url):
    ''' Serve or parse a form. '''
    if request.method == 'GET':
        return render_template(template_name)
    elif request.method == 'POST':
        with get_db() as db:
            form = request.form
            db.add(get_object_from_form(form))
            return redirect(redirect_url)
    else:
        abort(405)

@tournaments.route('/tournament/new/', methods=['GET', 'POST'])
def division_new():
    ''' Serve or parse a form to add a division. '''
    return serve_or_parse_form('tournaments/forms/division_new.html',
                               lambda f: Division(name=f['name']),
                               url_for('tournaments.admin'))


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

