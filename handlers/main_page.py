import webapp2

form ="""
<form>
	<a href="/blog">Web Development Blog</a>
	<br>
	<br>
	<b style="font-size:20px"> UNIT 2 </b>
	<br> <br>
	<a href="/unit2/rot13"> ROT 13 exercise </a>
	<br>
	<a href="/unit2/birthday"> Validation exercise (birthday) </a>
	<br>
	<a href="/unit2/signup"> Validation exercise2 (user signup) </a>
	<br><br>
	<b style="font-size:20px"> UNIT 3</b>
	<br> <br>
	<a href="/unit3/asciichan"> ASCII Chan </a>
</form>
"""

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write (form)	
    