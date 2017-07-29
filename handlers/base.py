
import re
import webapp2
import jinja2
import os,sys



CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import handy
from DB import User

template_dir = os.path.join(os.path.dirname(__file__), 'templates') 


#to load a jinja2 template from the file system
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'),autoescape=True)
jinja_env.globals.update(zip=zip)

"""
def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)"""


class Handler(webapp2.RequestHandler):
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kwargs):
		self.write(self.render_str(template, **kwargs))

	def write(self, *args, **kwargs):
		self.response.out.write(*args, **kwargs)

	def set_cookies(self, name, val):
		cookies_val = handy.make_secure_val(val)
		self.response.headers.add_header('Set-Cookie','%s=%s; Path=/' %(name,cookies_val))

	def read_cookies(self, name):
		cookies_val = self.request.cookies.get(name)
		if cookies_val and handy.check_secure_val(cookies_val):
			return handy.check_secure_val(cookies_val), cookies_val
	"""
	def check_login_status(self):
		if read_cookies(sel)
"""


	def login(self,id, name):
		self.set_cookies('user_id', str(id))
		#memcache.set(str(self.request.cookies.get('user_id')),name)	
		#print memcache.get(str(self.request.cookies.get('user_id')))

	def logout(self):
		self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

	
