import os
import webapp2
import jinja2
import hmac

SECRET = 'imsosecret'

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'),
								autoescape=True)

def hash_str(s):
	return hmac.new(SECRET,s).hexdigest()

def make_secure_val(s):
	return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
	val = h.split('|')[0]
	if h == make_secure_val(val):
		return val

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		#request object will have a cookies object. appengine will parsed http header and put all the cookies
		#into the dict-like objects. so, check whether key='visits' in it to get the value, or set it to be 0
		visits = 0
		visit_cookie_str = self.request.cookies.get('visits')
		if visit_cookie_str: #if not existing, then get None
			cookie_val = check_secure_val(visit_cookie_str)
			print(cookie_val)
			if cookie_val:
				visits = int(cookie_val)

		visits += 1
		
		new_cookie_val = make_secure_val(str(visits))

		self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val)
		#this cookie only exists in the browser! server doesn't know anything about it
		
		if visits > 1000 : 
			self.write("You are the best!")
		else: 
			self.write("You've been here %s times!" % visits)

app = webapp2.WSGIApplication([('/', MainPage)], debug = True)