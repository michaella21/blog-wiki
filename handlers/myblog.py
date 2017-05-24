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

class Blog(db.Model):
	subject = db.StringProperty(required = True)
	blog = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	

class BlogFront(Handler):
	def render_front(self,subject="", blog=""):
		
		blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 10")

		self.render("blog_front.html", subject = subject, blog = blog, blogs= blogs)

	def get(self):
		self.render_front()

	

class BlogNewPost(Handler):
	def render_form(self, subject="", blog="", error=""):

		self.render("blog_form.html", subject= subject, blog= blog, error=error)

	def get(self):
		self.render_form()

	def post(self):
		subject = self.request.get("subject")
		blog = self.request.get("content")
		created_date = self.request.get("created_date")

		if subject and blog: 
			b = Blog(subject = subject, blog = blog)
			
			b.put()
			time.sleep(1.0)
			b_id = b.key().id()
			

			self.redirect("/blog/%d" % b_id)

		else:
			error = "subject and content, please"
			self.render_form(subject, blog, error)

class BlogPermalink(BlogFront):
	def get(self,b_id):
		self.render("blog_front.html", blogs=[Blog.get_by_id(int(b_id))])




			