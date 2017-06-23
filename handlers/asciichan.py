import os
import webapp2
import jinja2
import time
import urllib2
import json
import logging
from xml.dom import minidom

from google.appengine.api import memcache
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

#using api from hostip, which doesn't work any more, so use a different website with json 
"""IP_url= "http://api.hostip.info/?ip="
def get_coords(ip):
	pass
	url = IP_url +ip
	content = None
	try:
		content = urllib2.urlopen(url).read()
	except urllib2.URLError: 
		return
	if content:
		#parse the xml and find the coordinate
		d = minidom.parseString(content)
		coords_node= d.getElementsByTagName("gml:coordinates")
		lon, lat = str(coords_node[0].firstChild.data).split(',')
		return db.GeoPt(lat, lon) """

#look up the location by ip address		
IP_url = "http://ip-api.com/json/"
def get_coords(ip):
	url = IP_url + ip
	content = None
	try:
		content = urllib2.urlopen(url).read()
	except urllib2.URLError:
		return
	if content:
		d =  json.loads(content)
		lat, lon = d['lat'], d['lon']
		return db.GeoPt(lat,lon)

#from the ip address given get_coords(ip), map it to google maps
GMAPS_url = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"
def gmaps_img(points):
	markers = '&'.join('markers=%s,%s' %(point.lat, point.lon) for point in points)
	return GMAPS_url + markers


def top_arts(update = False):
	key = 'top'
	arts = memcache.get(key)
	if arts is None or update:

		logging.error("DB QUERY")
		arts = db.GqlQuery("SELECT * FROM Art Order by created DESC LIMIT 10")

		#need to iterate over arts and we do not want to run multiple queries. 
		
		arts = list(arts)
		memcache.set(key, arts)
	return arts


#Create entities (store art entered in Datastore)
class Art(db.Model):
	title = db.StringProperty(required = True)
	#must be submitted, without it, will get exception. Always good to have reasonable constratints
	#to prevent you from adding bad data into your db. 
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)#automatically adding the current time
	coords = db.GeoPtProperty()

class Asciichan(Handler):
	def render_front(self, title="", art="", error=""):
		arts = top_arts() # cached arts by defining top_arts function
		

		#find which arts have coords
		#can use grnerator: filter(None) means return everything but none			
		points = filter (None, (a.coords for a in arts))
		#self.write(repr(points)) to check whether it works properly

		#if we have any arts with coords, make an image url, display the img url
		img_url = None
		if points:
			img_url = gmaps_img(points)

		self.render("ascii_front.html", title = title, art = art, error = error, arts = arts, img_url = img_url)

	


	def get(self):
		self.render_front()

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")

		if title and art:
			a = Art(title = title, art = art )
			#lookup the user's coordinates from their IP
			
			coords = get_coords(self.request.remote_addr)#request ip address
			#if we have coordinates, add them to art.
			
			if coords:
				a.coords = coords
			 
			a.put()
			#fix stale cache, it's fine here since we have only one key now (CACHE['top'])
			#CACHE.clear() 
			#Simple cleaing above can cause cache stampede so let's use update
			#return the querry and update the cache
			top_arts(True)
			time.sleep(1.0)

			self.redirect("/unit3/asciichan")
		else:
			error = "We need both atitle and some art work!"	
			self.render_front(title, art, error)
