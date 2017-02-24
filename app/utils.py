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
    app.jinja_env.globals.update(upcoming_events=upcoming_events)
    app.jinja_env.globals.update(get_chals=get_chals)

def init_errors(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def general_error(error):
        return render_template('errors/500.html'), 500

def get_chals(eid):
    chals = Challenge.query.filter_by(eid=eid).all()
    return [chals[i:i+6] for i in range(0, len(chals), 6)]

def get_current_events():
    return Event.query.filter(Event.end >= datetime.now()).all()

def upcoming_events():
#Get the upcoming events for the next month
    now = int(time.time())
    events = requests.get('https://ctftime.org/api/v1/events/?limit={}&start={}&finish={}'.format(8, now, now + 2592000)).json()
    info = [{"name": event["title"], "url": event["url"]} for event in events]
    return [info[i:i+4] for i in range(0, len(info), 4)]
