
import webapp2
import cgi




form ="""
<form method="post">
	What is your birthday?
	<br>
	<br>

	<label> Month <input type="text" name="month" value ="%(month)s"></label>
	<label> Day <input type="text" name="day" value="%(day)s"></label>
	<label> Year <input type="text" name="year" value ="%(year)s"></label>
	<div style ="color: red"> %(error)s</div>
	<br>
	<br>
	<input type="submit">
</form>
"""
#witout specifying method=post, default is GET


class BirthdayHandler(webapp2.RequestHandler):
	def write_form(self, error="", month ="", day="", year=""):
		self.response.out.write(form %{"error": error, 
										"month": escape_html(month), 
										"day": escape_html(day), 
										"year": escape_html(year)})
    
	def get(self):
		self.write_form()

	
    	#self.response.headers['Content-Type'] = 'text/plain'
	def post(self):
    	# user_ : what user actually entered
		user_month = self.request.get('month')
		user_day = self.request.get('day')
		user_year = self.request.get('year')

		# can see whether it's valid or not
		month = valid_month(user_month)
		day = valid_day(user_day)
		year = valid_year(user_year)

		if not (month and day and year):
			self.write_form("That doesn't look valid to me, friend!", 
				user_month, user_day, user_year ) 
			#so now we give an error message 
			#WITH all the parameters that user entered instead of empty new form 
		else:
			self.redirect("/unit2/birthday/thanks") #don't need to add entire domain, we just 
			#redirect insider the same domain
class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Thanks! That's a totally valid day!")

months=['January', 'February', 'March', 'April', 'May', 'June',
 'July', 'August', 'September', 'October', 'November', 'December']

month_abbvs = dict((m[:3].lower(),m) for m in months)

def valid_month(month):
	if month:
		short_month = month[:3].lower()
		return month_abbvs.get(short_month)

def valid_day(day):
	if day and day.isdigit():
		if int(day) > 0 and int(day) <= 31:
			return day

def valid_year(year):
	if year and year.isdigit():
		if int(year) > 1900 and int(year) < 2020:
			return int(year)
def escape_html(s):
	return cgi.escape(s,quote=True)
