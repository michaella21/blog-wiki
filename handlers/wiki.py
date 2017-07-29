import os,sys
import webapp2
import jinja2
import logging
import time

from google.appengine.ext import db
from google.appengine.api import memcache


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import handy
import base
from DB import Wiki


class BaseHandler(base.Handler):
	def get_key(self):
		url = self.request.url

		if url.rsplit('/',1)[-1] == '_edit':
			return None
		else:
			return url.rsplit('/',1)[-1]



class WikiFront(BaseHandler):
	def get(self):
		w = Wiki.Wiki.by_name("wiki")
		self.render("wiki_front.html", wiki = w)


		
class WikiPage(BaseHandler):
	def get(self,term):
		key = self.get_key()
		w = Wiki.Wiki.by_name(key)
		
		if w:
			self.render("wiki_page.html", wiki = w)
		else:
			self.redirect("/wiki/_edit/"+key)
		

class WikiNewPost(BaseHandler):
	def __render_form(self, content ="", error ="", wiki=""):
		w = Wiki.Wiki.by_name(self.get_key())

		if w:
			self.render("wiki_post.html", content=w.content, wiki=w)
		else:
			self.render("wiki_post.html", wiki ="")

	def get(self,term):
		self.__render_form()

	def post(self,term):

		name = self.get_key()
		if not name:
			name = "wiki"

		content = self.request.get("content")
		created = self.request.get("created_date")

		if content:
			#check whether it's updating or new content:
			w = Wiki.Wiki.by_name(name)
			if w:
				w.content = content
				w.put()
			else:
				w = Wiki(name= name, content=content)
				w.put()

			
			r = Revision(name= name, content=content, wiki_id = w.key().id())
			r.put()
			time.sleep(1.0)
			if name == "wiki":
				name = ""
			self.redirect('/wiki/'+name)

		else:
			error = "Please provide the content."
			self.__render_form(content, error)

















