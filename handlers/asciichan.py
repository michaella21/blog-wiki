import os
import webapp2
import jinja2
import time

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'),
								autoescape=True)

class Handler(webapp2.RequestHandler):
	def write(self, *args, **kwargs):
		self.response.out.write(*args, **kwargs)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kwargs):
		self.write(self.render_str(template, **kwargs))

#Create entities (store art entered in Datastore)
class Art(db.Model):
	title = db.StringProperty(required = True)
	#must be submitted, without it, will get exception. Always good to have reasonable constratints
	#to prevent you from adding bad data into your db. 
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)#automatically adding the current time


class Asciichan(Handler):
	def render_front(self, title="", art="", error=""):
		arts = db.GqlQuery("SELECT * FROM Art Order by created DESC")

		self.render("ascii_front.html", title = title, art = art, error = error, arts = arts)


	def get(self):
		self.render_front()

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")

		if title and art:
			a = Art(title = title, art = art )
			a.put()
			time.sleep(1.0)

			self.redirect("/unit3/asciichan")
		else:
			error = "We need both atitle and some art work!"	
			self.render_front(title, art, error)
