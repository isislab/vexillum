from flask import session, render_template
from models import db, Event, Challenge
from datetime import datetime
import requests
import time

def logged_in():
    return bool(session.get('username', False))

def init_utils(app):
    #app.jinja_env.globals.update(logged_in=logged_in)
    app.jinja_env.globals.update(get_current_events=get_current_events)

def init_errors(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def general_error(error):
        return render_template('errors/500.html'), 500

def get_current_events():
    return Event.query.filter(Event.end >= datetime.now()).all()

def upcoming_events():
#Get the upcoming events for the next month
    now = int(time.time())
    events = requests.get('https://ctftime.org/api/v1/events/?limit={}&start={}&finish={}'.format(10, now, now + 2593000))
    return events
