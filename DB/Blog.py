

from google.appengine.ext import db
from google.appengine.api import memcache


class Blog(db.Model):
	subject = db.StringProperty(required = True)
	blog = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True) #this is not editable
	modified = db.DateTimeProperty(auto_now = True)

	def make_dict(self):
		d = {'subject': self.subject,
			'content': self.blog,
			'created': self.created.strftime('%c'),
			'last_modified': self.modified.strftime('%c')}
		return d
