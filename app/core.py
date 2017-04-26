from flask import render_template, request, redirect, url_for, session, Blueprint, flash, jsonify
from models import db, Event, Challenge, File, Entry, User, Config, WorkingOn
from utils import upload_file, is_setup, logged_in, collaborators
from passlib.hash import bcrypt_sha256 as bcrypt
from werkzeug import secure_filename
from datetime import datetime
import re
import os

core = Blueprint('core', __name__)

@core.before_request
def redirect_setup():
    if not is_setup() and request.path != "/setup":
	return redirect(url_for('core.setup'))

@core.route('/test')
def test():
    return jsonify(collaborators(1))

@core.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html')

@core.route('/setup', methods=['GET','POST'])
def setup():
    if not is_setup():
    	if request.method=='POST' and len(request.form)==5:
	    errors = []
	    if len(request.form['username']) > 0 and User.query.filter_by(name=request.form['username']).first():
		errors.append('This username is taken')
	    else:
		name = request.form['username']
	    
	    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", request.form['email']):
            	if User.query.filter_by(email=request.form['email']).first():
                    errors.append('This email has already been used')
            	else:
                    email = request.form['email']
	    else:
            	errors.append('Invalid email')
	    
	    if len(request.form['team_name']) > 0:
	    	team = request.form['team_name']
	    else:
		errors.append('Team name cannot be empty')
	    
	    if len(request.form['password']) > 0:
            	password = bcrypt.hash(request.form['password'])
            else:
            	errors.append('Password cannot be blank')

	    if len(errors) > 0:
		return jsonify(errors)
	    else:
		user = User(name, email ,password)
		user.admin = True
		db.session.add(user)
		db.session.add(Config('TEAM_NAME',team))
		db.session.add(Config('SETUP', "True"))
		db.session.commit()
    		return redirect(url_for('auth.login'))
    	return render_template('setup.html')
    return redirect(url_for('core.home'))

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
	#try:
        name = request.form['name']
        url = request.form['url']
        start = datetime.strptime(request.form['start'],'%Y-%m-%dT%H:%M')
        end = datetime.strptime(request.form['end'], '%Y-%m-%dT%H:%M')
        login = request.form['login']
        password = request.form['password']
	#except:
	    #errors.append("Error: missing one or more required fields")        

        if len(errors) > 0:
            return jsonify(errors)
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

@core.route('/update_event', methods=['GET','POST'])
def update_event():
    if request.method == 'POST' and len(request.form)==8:
        errors = []
	try:
	    name = request.form['name']
            url = request.form['url']
            start = datetime.strptime(request.form['start'],'%Y-%m-%dT%H:%M:%S')
            end = datetime.strptime(request.form['end'], '%Y-%m-%dT%H:%M:%S')
            login = request.form['login']
            password = request.form['password']
	except:
	    errors.append("Error: missing one or more required fields")        

        if len(errors) > 0:
            return redirect(url_for('core.home', errors=errors))
        else:
            event = Event.query.filter_by(eid=request.form['eid']).first()
            if event:
		event.name = name
		event.url = url
		event.start = start
		event.end = end
		event.login = login
		event.password = password
            	db.session.commit()
            	eid = event.eid
	    	flash("Successfully created event")
            	return redirect('/event/{}'.format(eid))
            db.session.close()
            return redirect(request.url)
    return redirect(request.url)


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

@core.route('/update_challenge', methods=['POST'])
def update_challenge():
    if request.method == 'POST' and len(request.form)==7:
	errors = []
	try:
	    eid = request.form['eid']
	    name = request.form['name']
	    category = request.form['category']
	    value = int(request.form['value'])
	    desc = request.form['description']
	except:
	    errors.append("Error: One or more fields missing or incorrect")
	
	if len(errors) > 0:
	    return "Failed to update challenge"
	else:
	    chal = Challenge.query.filter_by(cid=request.form['cid']).first()
	    if chal:
		chal.name = name
		chal.category = category
		chal.value = value
		chal.description = desc
	    	db.session.commit()
	    	cid = chal.cid
		
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
	    	return redirect('/challenge/{}'.format(cid))
	    db.session.close()
	    return redirect(request.url)
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

@core.route("/submit_flag", methods=['POST'])
def submit_flag():
    if request.method=='POST' and len(request.form)==3:
	errors = []
	try:
	    chal_id = request.form['cid']
	    flag = request.form['flag']
	    chal = Challenge.query.filter_by(cid=chal_id).first()
	except:
	    errors.append("Error: one or more required fields missing or invalid")

	if chal and len(errors)==0:
	    chal.flag = flag
	    chal.solved = True
	    db.session.commit()
	    db.session.close()
	    return redirect("/challenge/{}".format(chal_id))
	else:
	    return jsonify(errors)

@core.route('/working/<chal_id>')
def working(chal_id):
    if logged_in():
	chal = Challenge.query.filter_by(cid=chal_id).first()
	user = User.query.filter_by(name=session['username']).first()
	if chal and user:
	    work = WorkingOn.query.filter_by(cid=chal.cid).filter_by(uid=user.uid).first()
	    if work:
		work.working = True
	    else:
	    	work = WorkingOn(user.uid, chal.cid)
	    	db.session.add(work)
	    db.session.commit()
	    db.session.close()
	    return "Success"
	return "User or challenge not found"
    return redirect(url_for('auth.login'))

@core.route('/stop_working/<chal_id>')
def stop_working(chal_id):
    if logged_in():
	chal = Challenge.query.filter_by(cid=chal_id).first()
	user = User.query.filter_by(name=session['username']).first()
	if chal and user:
	    work = WorkingOn.query.filter_by(cid=chal.cid).filter_by(uid=user.uid).first()
	    if work:
		work.working = False
		db.session.commit()
		db.session.close()
		return "Success"
	    else:
		db.session.close()
		return "You are not working on this challenge"
	else:
	    db.session.close()
	    return "Challenge or user not found"
    return redirect(url_for('auth.login'))
