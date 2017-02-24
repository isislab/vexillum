from flask import *
import requests
import time

def logged_in():
    return bool(session.get('username', False))

def init_utils(app):
    app.jinja_env.globals.update(logged_in=logged_in)

def init_errors(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def general_error(error):
        return render_template('errors/500.html'), 500

def upcoming_events():
'''
Get the upcoming events for the next month
'''
    now = int(time.time())
    events = requests.get('https://ctftime.org/api/v1/events/?limit={}&start={}&finish={}'.format(10, now, now + 2593000))
    return events
