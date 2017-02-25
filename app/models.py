from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)
    joined = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, email, password):
	self.name = name
	self.email = email
	self.password = password

class Event(db.Model):
    eid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    url = db.Column(db.String(128))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    place = db.Column(db.Integer, default=None)
    login = db.Column(db.String(128), default=None)
    password = db.Column(db.String(128), default=None)
    archived = db.Column(db.Boolean, default=False)

    def __init__(self, name, url, start, end, login, password):
	self.name = name
	self.url = url
	self.start = start
	self.end = end
	self.login = login
	self.password = password


class Challenge(db.Model):
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eid = db.Column(db.Integer, db.ForeignKey('event.eid'))
    name = db.Column(db.String(64))
    category = db.Column(db.String(64))
    description = db.Column(db.Text)
    value = db.Column(db.Integer)
    flag = db.Column(db.String(64), default=None)
    solved = db.Column(db.Boolean, default=False)

    def __init__(self, eid, name, category, description, value):
	self.eid = eid
	self.name = name
	self.category = category
	self.description = description
	self.value = value

class WorkingOn(db.Model):
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey('challenge.cid'), primary_key=True)
    working = db.Column(db.Boolean, default=True)

    def __init__(self, uid, cid):
	self.uid = uid
	self.cid = cid

class File(db.Model):
    fid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cid = db.Column(db.Integer, db.ForeignKey('challenge.cid'))
    location = db.Column(db.Text)

    def __init__(self, cid, location):
	self.cid = cid
	self.location = location

class Entry(db.Model):
    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chal_id = db.Column(db.Integer, db.ForeignKey('challenge.cid'))
    entry_type = db.Column(db.Integer) #0=comment, 1=code, 2=file
    name = db.Column(db.Text)
    content = db.Column(db.Text, default=None) #only for text and codes
    location = db.Column(db.Text, default=None) #only for files

    def __init__(self, chal_id, entry_type, name, content=None, location=None):
	self.chal_id = chal_id
	self.entry_type = entry_type
	self.name = name
	self.content = content
	self.location = location


class Config(db.Model):
    kid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.Text)
    value = db.Column(db.Text)

    def __init__(self, key, value):
	self.key = key
	self.value = value

    def __repr__(self):
	print 'Key:{}, Value:{}'.format(self.key, self.value)
