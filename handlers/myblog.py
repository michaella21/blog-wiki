import os
import webapp2
import jinja2
import time
import datetime
import json
import logging

from google.appengine.ext import db
from google.appengine.api import memcache


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'),
								autoescape=True)
jinja_env.globals.update(zip=zip)

def top_blogs(update = False):
	key = 'top'
	blogs = memcache.get(key)
	if blogs is None or update is True: 
		logging.error("DB QUERY")
		blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 10")
		memcache.set('top_last_called', datetime.datetime.now())
		blogs = list(blogs)
		memcache.set(key, blogs)

	return blogs


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

	def flush(self):
		memcache.flush_all()

	def cache_age(self, key):
		since_queried = (datetime.datetime.now()-memcache.get(key)).total_seconds()
		query_time = "Queried %r seconds ago" % int(since_queried)
		return query_time



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
		blogs= top_blogs()
		b_ids = [blog.key().id() for blog in blogs]
				
		if self.request.url.endswith('.json'):
			self.render_json([blog.make_dict() for blog in blogs])
		else: #self.request.cookies.get('user_id'):
			#u = str(str(self.request.cookies.get('user_id')))
			self.render("blog_front.html", blogs= blogs, b_ids= b_ids, query_time = self.cache_age('top_last_called'))


		

class BlogNewPost(Handler):
	def __render_form(self, subject="", blog="", error=""):

		self.render("blog_form.html", subject= subject, blog= blog, error=error)

	def get(self):
		self.__render_form()

	def post(self):

		subject = self.request.get("subject")
		blog = self.request.get("content")
		created_date = self.request.get("created_date")

		if subject and blog: 
			b = Blog(subject = subject, blog = blog)
			
			b.put()
			
			time.sleep(1.0)
			top_blogs(True)
			b_id = b.key().id()
			key_blog = str(b_id)
			key_called = str(b_id)+'page_last_called'
			memcache.set(key_called, datetime.datetime.now())
			memcache.set(key_blog, b)

			self.redirect("/blog/%d" % b_id)

		else:
			error = "subject and content, please"
			self.__render_form(subject, blog, error)

class BlogPermalink(BlogFront):
	def get(self,b_id):
		blog = memcache.get(str(b_id))
		key_called = str(b_id)+'page_last_called'

		if self.request.url.endswith('.json'):
			self.render_json(blog.make_dict())
		if not blog:
			logging.error("DB QUERY")
			blog = Blog.get_by_id(int(b_id))
			key_blog = str(b_id)
			
			memcache.set(key_called, datetime.datetime.now())
			memcache.set(key_blog, blog)

		self.render("blog_permalink.html", blog=blog, b_id=b_id, query_time = self.cache_age(key_called))

class MemcacheFlush(Handler):
	def get(self):
		self.flush()
		self.redirect('/blog')





			