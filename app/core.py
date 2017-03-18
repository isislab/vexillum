from flask import render_template, request, redirect, url_for, session, Blueprint, flash, jsonify
from models import db, Event, Challenge, File, Entry
from utils import get_current_events, upcoming_events, get_chals, upload_file, get_entries, get_files
from werkzeug import secure_filename
from datetime import datetime
import os

core = Blueprint('core', __name__)

@core.route('/test')
def test():
    return jsonify(get_entries(1))

@core.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html')

@core.route('/event/<event_id>')
def event(event_id):
    event = Event.query.filter_by(eid=event_id).first()
    if event:
	return render_template('event.html', event=event)
    else:
	return "Error"

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
    event = Event.query.filter_by(eid=chal.eid).first()
    db.session.close()
    if chal and event:
	return render_template('challenge.html', chal=chal, event=event)
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

	    cid = new_chal.cid
	    #try:
	    files = request.files.getlist('file[]')
	    if files and len(files) > 0:
	    	for f in files:
	    	    if f and len(f.filename) > 0:
	    	        #try:
	    	        upload_file(f)
	    	        new_file = File(cid, f.filename)
	    		db.session.add(new_file)
	    		db.session.commit()
	    	        #except:
	    	    	#errors.append("Something went wrong")
	    	    else:
	    	        errors.append("Error: something wrong with the file or filename")
	    	#except:
	    	#    errors.append("No files recieved")

	    db.session.close()
	    return redirect('/event/{}'.format(eid))
    else:
	return "Failed to add challenge"

@core.route('/new_entry', methods=['POST'])
def new_entry():
    if request.method == 'POST':
	errors = []
	try:
	    entry_type = int(request.form['type'])
	except:
	    errors.append("Error: missing type")
	    flash("Error: missing type", "error")
	    return redirect('/challenge/{}'.format(request.form['cid']))

	chal_id = request.form['cid']
	name = request.form['name']

	if entry_type in range(0,2):
	    desc = request.form['description']
	    new_entry = Entry(chal_id, entry_type, name, desc,)
	elif entry_type == 2:
	    if 'file' in request.files:
		f = request.files['file']
		if f and len(f.filename) > 0:
		    try:
			upload_file(f)
			new_entry = Entry(chal_id, entry_type, name, None, f.filename)
		    except:
			errors.append("Something went wrong")
		else:
		    errors.append("Error: something wrong with the file or filename")
	    else:
		errors.append("No file recieved")
	else:
	    errors.append("Error: invalid type")
	if len(errors) > 0:
	    return str(errors)
	else:
	    db.session.add(new_entry)
	    db.session.commit()
	    db.session.close()
	    return redirect('/challenge/{}'.format(chal_id))
    else:
	return "Failed to add entry"   
