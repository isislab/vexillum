from urllib2 import Request, urlopen, URLError
import requests
import json

class Event:
	self.organizer
	self.onsite
	self.finish
	self.description
	self.weight
	self.title
	self.url
	self.is_votable_now
	self.restrictions
	self.format
	self.start
	self.participants
	self.ctftime_url
	self.location
	self.live_feed
	self.duration
	self.logo
	self.format_id
	self.id
	self.ctf_id


def init_utils(app):
    app.jinja_env.globals.update(signed_up=signed_up)
    app.jinja_env.globals.update(joined_group=joined_group)
    app.jinja_env.globals.update(check_rated=check_rated)

def init_errors(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def general_error(error):
        return render_template('errors/500.html'), 500

def upcoming():
	a = Event()
	
	upcomingctfs = requests.get('https://ctftime.org/api/v1/events/?limit=100&start=1487193282&finish=1489536000')
	upcomingctfs_string = str(upcomingctfs.json())
	print (upcomingctfs_string)

upcoming()

