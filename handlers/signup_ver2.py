#!/usr/bin/env python

import os
import re
import hmac
import hashlib
import random
import time
import logging
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db
from google.appengine.api import memcache


secret = "mittens"


#template_dir is the parent directory of the directory where program resides.
template_dir = os.path.join(os.path.dirname(__file__), 'templates') 


#to load a jinja2 template from the file system
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'),autoescape=True)

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)

#Password stored as 5-character salt + shat256
def make_salt(length = 5):
	return ''.join(random.choice(letters) for i in range(length))

def make_pw_hash(name, pw, salt=None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(str(name) + str(pw) + str(salt)).hexdigest()
	return '%s,%s' %(h, salt)

def valid_pw(name, pw, h):
	salt = h.split(',')[1]
	return h == make_pw_hash(name, pw, salt)

#Cookies stored as cookie_name = make_secure_val(val)
def make_secure_val(val):
	return "%s|%s" % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
	val = secure_val.split('|')[0]
	if make_secure_val(val) == secure_val:
		return val

#Regular expressions: check the vaildity of user inputs
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

def valid_username(username):
	return username and USER_RE.match(username)

def valid_password(password):
	return password and PASS_RE.match(password)

def valid_email(email):
	return not email or EMAIL_RE.match(email)



class BaseHandler(webapp2.RequestHandler):
	def render(self, template, **kwargs):
		self.response.out.write(render_str(template, **kwargs))

	def write(self, *args, **kwargs):
		self.response.out.write(*args, **kwargs)

	def set_cookies(self, name, val):
		cookies_val = make_secure_val(val)
		self.response.headers.add_header('Set-Cookie','%s=%s; Path=/' %(name,cookies_val))

	def read_cookies(self, name):
		cookies_val = self.request.cookies.get(name)
		if cookies_val and check_secure_val(cookies_val):
			return check_secure_val(cookies_val), cookies_val

	def login(self,id, name):
		self.set_cookies('user_id', str(id))
		#memcache.set(str(self.request.cookies.get('user_id')),name)	
		#print memcache.get(str(self.request.cookies.get('user_id')))

	def logout(self):
		self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')


	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		if self.read_cookies('user_id'):
			uid = int(self.read_cookies('user_id')[0])
			self.user = User.by_id(uid)

			

class Signup(BaseHandler):
	def get(self):
		self.render("signup.html")

	def post(self):
		have_error = False
		self.username = self.request.get('username')
		self.password = self.request.get('password')
		self.verify = self.request.get('verify')
		self.email = self.request.get('email')

		params = dict(username = self.username, email = self.email)


		if not valid_username(self.username):
			params['error_username'] = "That's not a valid username."
			have_error = True

		if not valid_password(self.password):
			params['error_password'] = "That wasn't a valid password."
			have_error = True
		elif self.password != self.verify:
			params['error_verify'] = "Your passwords didn't match."
			have_error = True

		if not valid_email(self.email):
			params['error_email'] = "That's not a valid email."
			have_error = True

		if have_error:
			self.render('signup.html', **params)
		else:
			self.done()

	# Need to be implemented specifically in subclasses		
	def done(self, *a, **kw):
		raise NotImplementedError

			
class Signup_ver1(Signup):
	def done(self):
		self.redirect('/unit2/welcome?username=' + self.username)

class Registration(Signup):
	def done(self):
		#check whether the user is already in the database
		u = User.by_name(self.username)
		print u, self.username
		if u:
			msg = "That user already exists."
			self.render('signup.html',error_username = msg)

		else:
			u = User.register(self.username, self.password, self.email)
			u.put()
			u_id=u.key().id()
			self.login(u_id, self.username)
			self.redirect('/blog/welcome')

class Login(BaseHandler):
	def get(self):
		self.render("login.html")

	def post(self):
		self.username = self.request.get("username")
		self.password = self.request.get("password")

		
		logging.error("DB QUERY")
		u = User.login(self.username, self.password)		

		if u:
			self.login(u[1],u[0])
			self.redirect('/blog')
		
		else:
			self.render('login.html', error_login = "Invalid Login")

class Logout(BaseHandler):
	def get(self):
		self.logout()
		self.redirect('/blog')

# USER DB model 
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
		pw_hash = make_pw_hash(name,pw)
		return User(parent = users_key(),
					name = name,
					pw_hash = pw_hash,
					email = email
					)

	@classmethod
	#Check whether the name and pw match with what we have in DB.
	def login(cls, name, pw):
		u = cls.by_name(name)
		if u and valid_pw(name = name, pw = pw, h = u.pw_hash):
			#memcache.set(u.name, [u.key().id(), u.pw_hash])
			return u.name, u.key().id()
	
		else:
			return None

#you can get a new key object from an ancestor path
def users_key(group = 'default'):
	return db.Key.from_path('users',group)


class Welcome(BaseHandler):
	def get(self):
		username = self.request.get('username')
		if valid_username(username):
			self.render('welcome.html', username = username)
		else:
			self.redirect('/unit2/signup')

class Welcome_ver2(BaseHandler):
	def get(self):
		if BaseHandler.read_cookies(self,'user_id'):
			username = self.user.name
			self.render('welcome.html', username = username)
			
		else: 
			self.redirect('/blog/signup')



 







										