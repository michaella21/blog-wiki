import os
import webapp2
import jinja2
import time
import json

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'),
								autoescape=True)
jinja_env.globals.update(zip=zip)


class Handler(webapp2.RequestHandler):
	def write(self, *args, **kwargs):
		self.response.out.write(*args, **kwargs)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kwargs):
		self.write(self.render_str(template, **kwargs))

	def render_json(self,dict):
		json_contents = json.dumps(dict)
		self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
		self.write(json_contents)


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

	

class BlogFront(Handler):
	def get(self):
		blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 10")
		b_ids = [blog.key().id() for blog in blogs]

		if self.request.url.endswith('.json'):
			self.render_json([blog.make_dict() for blog in blogs])
		else:
			self.render("blog_front.html", blogs= blogs, b_ids= b_ids)
		

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
		blog = Blog.get_by_id(int(b_id))

		if not blog:
			self.error(404)
		elif self.request.url.endswith('.json'):
			self.render_json(blog.make_dict())
		else:
			self.render("blog_permalink.html",blog=blog, b_id=b_id)






			