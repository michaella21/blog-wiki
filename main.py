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


import webapp2
import cgi
import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), "handlers"))
sys.path.append(os.path.join(os.path.dirname(__file__),"templates"))
sys.path.append('/Library/Python/2.7/site-packages')


from rot13 import *
from birthday import *
from signup import *
from asciichan import *
from myblog import *
from signup_ver2 import *
from wiki import *
from main_page import form, MainHandler
"""
def handle_404(self, request, response, exception):
		logging.exception(exception)
		self.redirect("/wiki/")
		response.set_status(404)
"""
PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

app = webapp2.WSGIApplication([('/', MainHandler), 
								('/unit2/birthday', BirthdayHandler),
								('/unit2/birthday/thanks',ThanksHandler),
								('/unit2/rot13', Rot13Handler), 
								('/unit2/signup', Signup_ver1), 
								('/unit2/welcome', Welcome),
								('/unit3/asciichan', Asciichan),
								('/blog/signup', Registration),
								('/blog/welcome', Welcome_ver2),
								('/blog/login', Login),
								('/blog/logout', Logout),
								('/blog/?(?:.json)?',BlogFront),
								('/blog/newpost', BlogNewPost),
								('/blog/flush', MemcacheFlush),
								('/blog/([0-9]+)(?:.json)?', BlogPermalink),
								('/wiki/?', WikiFront),
								('/wiki/_edit'+PAGE_RE, WikiNewPost),
								('/wiki'+PAGE_RE, WikiPage),
								], debug=True)

#app.error_handlers[404] = handle_404


""" () looking for a group of things, ?: means 'don't send it to a handler as a parameter
so in permalink case, /blog/numbers (and optionally ends with .json)

/blog/? will match both /blog and /blog/
what if it can frequently face a case like "//..+..", one way to solve can be redirect the multiple slash cases to 
single/no slash (\w+)('/wiki/(\w+)?', WikiNewPost),([a-zA-Z0-9_]*)
"""



