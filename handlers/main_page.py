import webapp2

form ="""
<form>
	<a href="/blog">Blog</a>
	<br>
	<a href="/wiki">Wiki page</a>
	<br><br>
	<b style="font-size:18px"> WebDev course related </b>
	<br> <br>
	<a href="/unit2/rot13"> ROT 13 exercise </a>
	<br>
	<a href="/unit2/birthday"> Validation exercise (birthday) </a>
	<br>
	<a href="/unit2/signup"> Validation exercise2 (user signup) </a>
	<br>
	<a href="/unit3/asciichan"> ASCII Chan </a>
	<br>
	<a href="/blog/signup"> Authentification exercise (user signup) </a>
	<br>
	<a href="/blog/login"> Authentification exercise (login) </a>
	<br>
	<a href="/blog/.json"> JSON output (API) </a>
	

</form>
"""

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write (form)	
    