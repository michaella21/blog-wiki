
from google.appengine.ext import db
from google.appengine.api import memcache


class Wiki(db.Model):
	name = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True) #this is not editable
	modified = db.DateTimeProperty(auto_now = True)

	def make_dict(self):
		d = {'name': self.name,
			'content': self.content,
			'created': self.created.strftime('%c'),
			'last_modified': self.modified.strftime('%c')}
		return d

	@classmethod
	def by_name(cls, name):
		w = Wiki.all().filter('name =', name).get()
		return w


#Insert only, keep all the revision history with the macthing id of Wiki 
class Revision(db.Model):
	name = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True) #when the revision is made
	wiki_id = db.IntegerProperty(required = True)#to identify which wiki page is connected to

