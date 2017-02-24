from flask import render_template, request, redirect, url_for, session, Blueprint
from models import Event, Challenge, File
from datetime import datetime

core = Blueprint('core', __name__)

@core.route('/')
def home():
    return render_template('index.html')

@core.route('/events')
def events():
    return "TODO"

@core.route('/event/<event_id>')
def event(event_id):
    return "TODO"

@core.route('/new_event', methods=['GET','POST'])
def new_event():
    #if request.method == 'POST':
    #    #do stuff
    #    pass
    #else:
    #    return redirect(url_for('core.events'))
    if request.method == 'POST' and len(request.form)==7:
	errors = []
	try:
	    name = request.form['name']
	    url = request.form['url']
	    start = datetime.strptime(request.form['start'],'%Y-%m-%dT%I:%M')
	    end = datetime.strptime(request.form['end'], '%Y-%m-%dT%I:%M')
	    login = request.form['login']
	    password = request.form['password']
	except:
	    errors.append("Error: missing one or more required fields")
	
	if len(errors) > 0:
	    return render_template('create_event.html', errors=errors)
	else:
	    new_event = Event(name, url, start, end, login, password, event)
	    db.session.add(new_event)
	    db.session.commit()
	    eid = new_event.eid
	    db.session.close()
	    return redirect(url_for('core.event', event_id=eid))
    else:
	return render_template('create_event.html')

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
    
