#!/usr/bin/env python

import os
import re
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db


#template_dir is the parent directory of the directory where program resides.
template_dir = os.path.join(os.path.dirname(__file__), 'templates') 


#to load a jinja2 template from the file system
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'),autoescape=True)

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)
"""
def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)
"""
class BaseHandler(webapp2.RequestHandler):
	def render(self, template, **kwargs):
		self.response.out.write(render_str(template, **kwargs))

	def write(self, *args, **kwargs):
		self.response.out.write(*args, **kwargs)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

PASS_RE = re.compile(r"^.{3,20}$")

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

def valid_username(username):
	return username and USER_RE.match(username)

def valid_password(password):
	return password and PASS_RE.match(password)

def valid_email(email):
	return not email or EMAIL_RE.match(email)

class Signup(BaseHandler):

	def get(self):
		self.render("signup.html")

	def post(self):
		have_error = False
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')

		params = dict(username = username, email = email)


		if not valid_username(username):
			params['error_username'] = "That's not a valid username."
			have_error = True

		if not valid_password(password):
			params['error_password'] = "That wasn't a valid password."
			have_error = True
		elif password != verify:
			params['error_verify'] = "Your passwords didn't match."
			have_error = True

		if not valid_email(email):
			params['error_email'] = "That's not a valid email."
			have_error = True

		if have_error:
			self.render('signup.html', **params)
		else:
			self.redirect('/unit2/welcome?username=' + username)

class Welcome(BaseHandler):
	def get(self):
		username = self.request.get('username')
		if valid_username(username):
			self.render('welcome.html', username = username)
		else:
			self.redirect('/unit2/signup')


 







										