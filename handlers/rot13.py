#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# "http://www.google.com/search"

import webapp2
import cgi


form ="""
<form method="post">
	<b style ="font-size: 30px"> Enter some text to ROT13 </b>
	<br>
	<br>
	<textarea name="text" value="%(contents)s" rows="10" cols="80">%(contents)s</textarea>
	<br>
	<br>
	<input type="submit">
</form>
"""
#witout specifying method=post, default is GET

class Rot13Handler(webapp2.RequestHandler):
	def write_form(self, contents=""):
		self.response.out.write(form %{"contents":contents})

	def get(self):
    	#self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write(form)
		self.write_form()

	def post(self):
		user_contents = self.request.get('text')
		typed_in = escape_html(rot13(user_contents))
		if user_contents == typed_in:
			self.write_form(escape_html(rot13(typed_in)))
		else:
			self.write_form(typed_in)
		

"""
class TestHandler(webapp2.RequestHandler):
	def post(self):
		#q = self.request.get("q") 
		#self.response.out.write(q)
		
		self.response.headers['Content-Type'] = 'text/plain' 
		#otherwise browswer will expect to see HTML from the testform
		self.response.out.write(self.request)
		#instead of defining separate variable like 'q', 
		#just used the obj itself
		#It's the very common way to debug 
"""


def escape_html(s):
	return cgi.escape(s,quote=True)

upper = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
lower = list('abcdefghijklmnopqrstuvwxyz')
alpha_dict={}


for i in range(26):
	alpha_dict[upper[i]] = upper[i-13]
	alpha_dict[lower[i]] = lower[i-13]



def rot13(s):
	for i in range(len(s)):
		if s[i] in alpha_dict:
			s = s[:i]+alpha_dict[s[i]]+s[i+1:]
	return s






