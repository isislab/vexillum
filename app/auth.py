from flask import render_template, request, redirect, url_for, session, Blueprint, flash, jsonify
from models import db, Event, Challenge, File, Entry, User, Config, Invite
from utils import logged_in
from passlib.hash import bcrypt_sha256 as bcrypt
import re

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if not logged_in():
        if request.method=='POST' and len(request.form)==3:
            errors = []
            user = User.query.filter_by(name=request.form['username']).first()
            db.session.close()
            if user and bcrypt.verify(request.form['password'], user.password):
                session['username'] = user.name
		if user.admin:
		    session['admin'] = True
		else:
		    session['admin'] = False
		flash("Login Successful")
		return redirect(url_for('core.home'))
	    flash("Username or password incorrect")
            return redirect(url_for('auth.login'))
        return render_template('login.html')
    else:
	return redirect(url_for('core.home'))

@auth.route('/logout')
def logout():
    if logged_in():
	session.clear()
    return redirect(url_for('core.home'))

@auth.route('/register', methods=['GET','POST'])
def register():
    if not logged_in():
        if request.method == 'GET':
            if request.args.get('token'):
                return render_template('register.html', token=request.args.get('token'))
        elif request.method=='POST' and len(request.form)==5:
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
	    
	    if len(request.form['token']) > 0:
	    	invite = Invite.query.filter_by(token=request.form['token']).first()
		if invite and not invite.expired():
		    invite.used = True
		else:
		    errors.append('Token is invalid or may have expired')
	    else:
		errors.append('Token cannot be empty')
	    
	    if len(request.form['password']) > 0:
            	password = bcrypt.hash(request.form['password'])
            else:
            	errors.append('Password cannot be blank')

	    if len(errors) > 0:
		return jsonify(errors)
	    else:
		user = User(name, email ,password)
		db.session.add(user)
		db.session.commit()
		db.session.close()
    		return redirect(url_for('auth.login'))
        return render_template('register.html')
    return redirect(url_for('core.home'))

@auth.route('/invite')
def invite():
    if logged_in():
	invite = Invite()
	db.session.add(invite)
	db.session.commit()
	token = invite.token
	db.session.close()
	return token
    return redirect(url_for('auth.login'))
