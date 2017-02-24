from flask import render_template, request, redirect, url_for, session, Blueprint, flash, jsonify
from models import db, Event, Challenge, File
from utils import get_current_events, upcoming_events, get_chals
from datetime import datetime

core = Blueprint('core', __name__)

@core.route('/test')
def test():
    return str(get_chals(1))

@core.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html')

@core.route('/events')
def events():
    return "TODO"

@core.route('/event/<event_id>')
def event(event_id):
    return render_template('event.html', event_id=event_id)

@core.route('/new_event', methods=['POST'])
def new_event():
    if request.method == 'POST' and len(request.form)==7:
        errors = []
	try:
            name = request.form['name']
            url = request.form['url']
            start = datetime.strptime(request.form['start'],'%Y-%m-%dT%H:%M')
            end = datetime.strptime(request.form['end'], '%Y-%m-%dT%H:%M')
            login = request.form['login']
            password = request.form['password']
	except:
	    errors.append("Error: missing one or more required fields")        

        if len(errors) > 0:
            return redirect(url_for('core.home', errors=errors))
        else:
            new_event = Event(name, url, start, end, login, password)
            db.session.add(new_event)
            db.session.commit()
            eid = new_event.eid
            db.session.close()
	    flash("Successfully created event")
            return redirect('/event/{}'.format(eid))
    else:
        return redirect(url_for('core.home'))

@core.route('/challenge/<chal_id>')
def challenge(chal_id):
    chal = Challenge.query.filter_by(cid=chal_id).first()
    if chal:
	return render_template('challenge.html', chal=chal)
    else:
	return "Error"

@core.route('/new_challenge', methods=['POST'])
def new_challenge():
    if request.method == 'POST' and len(request.form)==6:
	errors = []
	#try:
	eid = request.form['eid']
	name = request.form['name']
	category = request.form['category']
	value = int(request.form['value'])
	desc = request.form['description']
	#except:

    if len(errors) > 0:
    	return "Failed to add challenge"
    else:
	new_chal = Challenge(eid, name, category, desc, value)
	db.session.add(new_chal)
	db.session.commit()
	return redirect('/event/{}'.format(eid))
    
