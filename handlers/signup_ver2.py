#!/usr/bin/env python

import os,sys
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

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import handy
import base
from DB import User


#template_dir is the parent directory of the directory where program resides.
template_dir = os.path.join(os.path.dirname(__file__), 'templates') 


#to load a jinja2 template from the file system
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'),autoescape=True)


class BaseHandler(base.Handler):

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		if self.read_cookies('user_id'):
			uid = int(self.read_cookies('user_id')[0])
			self.user = User.User.by_id(uid)

			

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


		if not handy.valid_username(self.username):
			params['error_username'] = "That's not a valid username."
			have_error = True

		if not handy.valid_password(self.password):
			params['error_password'] = "That wasn't a valid password."
			have_error = True
		elif self.password != self.verify:
			params['error_verify'] = "Your passwords didn't match."
			have_error = True

		if not handy.valid_email(self.email):
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
		u = User.User.by_name(self.username)
		print u, self.username
		if u:
			msg = "That user already exists."
			self.render('signup.html',error_username = msg)

		else:
			u = User.User.register(self.username, self.password, self.email)
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
		u = User.User.login(self.username, self.password)		

		if u:
			self.login(u[1],u[0])
			self.redirect('/blog')
		
		else:
			self.render('login.html', error_login = "Invalid Login")

class Logout(BaseHandler):
	def get(self):
		self.logout()
		self.redirect('/blog')



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



 







										