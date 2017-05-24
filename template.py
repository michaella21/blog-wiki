import os
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'),
								autoescape = True)

"""
What's worng with this code? 
1. Hard to change- we hard coded with %s and we'r doing 
	complcated logic to put things together.
2. We don't get syntax highlighting, since we put html code in python.
	i.e., we don't deal with html and what we deal with is a big string,
	which is tedious to manipulate. 
3. It's error prone. For any kind of %s's, if we miss, it will show up. 
4. and this code is UGLY and not fun.

-> It will work for sure, for a small work. But it's not a very good 
approach to generate html pages for a general web application.
"""

 


class Handler(webapp2.RequestHandler):
	def write(self, *args, **kwargs):
		self.response.out.write(*args, **kwargs)

	#load our file(template) to generate jinja template (string)
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		items = self.request.get_all("food")
		self.render("shopping_list.html", items = items)


		
		

class FizzBuzzHandler(Handler):
	def get(self):
		n = self.request.get("n", 0)
		#n = n and int(n) #meaning, if n: n = int(n)
		if n:
			n = int(n)
		self.render('fizzbuzz.html', n = n)


app = webapp2.WSGIApplication([('/', MainPage), ('/fizzbuzz.*', FizzBuzzHandler),], debug=True)



