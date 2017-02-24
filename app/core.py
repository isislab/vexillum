from flask import render_template, request, redirect, url_for, session, Blueprint, flash
from models import db, Event, Challenge, File
from utils import get_current_events
from datetime import datetime

core = Blueprint('core', __name__)

@core.route('/test')
def test():
    return str(get_current_events())

@core.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html')

@core.route('/events')
def events():
    return "TODO"

@core.route('/event/<event_id>')
def event(event_id):
    return "TODO"

@core.route('/new_event', methods=['POST'])
def new_event():
    if request.method == 'POST' and len(request.form)==7:
        errors = []
	#try:
        name = request.form['name']
        url = request.form['url']
        start = datetime.strptime(request.form['start'],'%Y-%m-%dT%H:%M')
        end = datetime.strptime(request.form['end'], '%Y-%m-%dT%H:%M')
        login = request.form['login']
        password = request.form['password']
	#except:
	#    errors.append("Error: missing one or more required fields")        

        if len(errors) > 0:
            return redirect(url_for('core.home', errors=errors))
        else:
            new_event = Event(name, url, start, end, login, password)
            db.session.add(new_event)
            db.session.commit()
            eid = new_event.eid
            db.session.close()
	    flash("Successfully created event")
            return redirect(url_for('core.home'))
    else:
        return redirect(url_for('core.home'))

#@core.route('/challenge/<chal_id>')
@core.route('/challenge')
def challenge():
    return render_template('challenge.html')

@core.route('/new_challenge', methods=['GET','POST'])
def new_challenge():
    #if request.method == 'POST':
    #    #do stuff
    #    pass
    #else:
    #    return redirect(url_for('core.events'))
    if request.method == 'POST':
	return str(request.form)
    else:
    	return render_template('add_challenge.html')
    
