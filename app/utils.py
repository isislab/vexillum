from flask import session, render_template
from models import db, Event, Challenge, Entry, File, Config, WorkingOn, User
from werkzeug import secure_filename
from datetime import datetime, timedelta
import requests
import time
import os

def logged_in():
    return bool(session.get('username', False))

def init_utils(app):
    app.jinja_env.globals.update(logged_in=logged_in)
    app.jinja_env.globals.update(get_current_events=get_current_events)
    app.jinja_env.globals.update(get_past_events=get_past_events)
    app.jinja_env.globals.update(upcoming_events=upcoming_events)
    app.jinja_env.globals.update(get_chals=get_chals)
    app.jinja_env.globals.update(get_entries=get_entries)
    app.jinja_env.globals.update(get_files=get_files)
    app.jinja_env.globals.update(collaborators=collaborators)

def init_errors(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def general_error(error):
        return render_template('errors/500.html'), 500

def get_files(cid):
    files = File.query.filter_by(cid=cid).all()
    db.session.close()
    return files

def tdelta2str(delta):
    if isinstance(delta, timedelta):
	if delta.seconds < 60:
	    return "{} seconds ago".format(delta.seconds)
	elif delta.seconds/60 < 60:
	    return "{} minutes ago".format(delta.seconds/60)
	elif delta.seconds/60/60 < 24:
	    return "{} hours ago".format(delta.seconds/60/60)
	else:
	    return "{} days ago".format(delta.seconds/60/60/24)
    return None

def get_entries(cid):
    #comments = Entry.query.filter_by(chal_id=cid).filter_by(entry_type=0).all()
    #code = Entry.query.filter_by(chal_id=cid).filter_by(entry_type=1).all()
    #files = Entry.query.filter_by(chal_id=cid).filter_by(entry_type=2).all()
    #return {"comments": comments, "code": code, "files": files}
    entries = Entry.query.filter_by(chal_id=cid).order_by(Entry.added)
    return [ {"name": e.name, "type": e.entry_type, "content": e.content, "location": e.location, "added": tdelta2str(datetime.now()-e.added)} for e in entries]

def get_chals(eid):
    chals = Challenge.query.filter_by(eid=eid).all()
    return [chals[i:i+4] for i in range(0, len(chals), 4)]

def get_current_events():
    return Event.query.filter(Event.end >= datetime.now()).all()

def get_past_events():
    return Event.query.filter(Event.end < datetime.now()).all()

def upcoming_events():
#Get the upcoming events for the next month
    now = int(time.time())
    events = requests.get('https://ctftime.org/api/v1/events/?limit={}&start={}&finish={}'.format(8, now, now + 2592000)).json()
    info = [{"name": event["title"], "url": event["url"]} for event in events]
    return [info[i:i+2] for i in range(0, len(info), 2)]

def upload_file(f):
    if not os.path.exists('app/static/uploads'):
        os.makedirs('app/static/uploads')
    f.save(os.path.join('app','static','uploads', secure_filename(f.filename)))

def is_setup():
    s = Config.query.filter_by(key="SETUP").first()
    if s and s.value=="True":
	return True
    return False

def collaborators(chal_id):
    people = WorkingOn.query.filter_by(cid=chal_id).filter_by(working=True).all()
    return [User.query.filter_by(uid=p.uid).first().name for p in people]
