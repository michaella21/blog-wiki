import os, sys


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from google.appengine.ext import db
from google.appengine.api import memcache

import handy

class User(db.Model):
	name = db.StringProperty(required = True)
	pw_hash = db.StringProperty(required = True)
	email = db.StringProperty()

	@classmethod
	def by_name(cls, name):
		u = User.all().filter('name =', name).get()
		return u

	@classmethod
	def by_id(cls,uid):
		#Retrieves the model instance for the given numeric ID
		return User.get_by_id(uid, parent = users_key()) 

	@classmethod
	def register(cls, name, pw, email = None):
		pw_hash = handy.make_pw_hash(name,pw)
		return User(parent = users_key(),
					name = name,
					pw_hash = pw_hash,
					email = email
					)

	@classmethod
	#Check whether the name and pw match with what we have in DB.
	def login(cls, name, pw):
		u = cls.by_name(name)
		if u and handy.valid_pw(name = name, pw = pw, h = u.pw_hash):
			#memcache.set(u.name, [u.key().id(), u.pw_hash])
			return u.name, u.key().id()
	
		else:
			return None



#you can get a new key object from an ancestor path
def users_key(group = 'default'):
	return db.Key.from_path('users',group)