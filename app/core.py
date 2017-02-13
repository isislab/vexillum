from flask import render_template, request, redirect, url_for, session, Blueprint


core = Blueprint('core', __name__)

@core.route('/')
def home():
    return render_template('base.html')

@core.route('/api/upcoming_events')
def upcoming_events():
    return "TODO"
