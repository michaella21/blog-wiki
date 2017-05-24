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

sys.path.append(os.path.join(os.path.dirname(__file__), "handlers"))
sys.path.append(os.path.join(os.path.dirname(__file__),"templates"))
sys.path.append('/Library/Python/2.7/site-packages')


from rot13 import *
from birthday import *
from signup import *
from asciichan import *
from myblog import *
from main_page import form, MainHandler



app = webapp2.WSGIApplication([('/', MainHandler), 
								('/unit2/birthday', BirthdayHandler),
								('/unit2/birthday/thanks',ThanksHandler),
								('/unit2/rot13', Rot13Handler), 
								('/unit2/signup', Signup), 
								('/unit2/welcome', Welcome),
								('/unit3/asciichan', Asciichan),
								('/blog/?',BlogFront),
								('/blog/newpost', BlogNewPost),
								('/blog/([0-9]+)', BlogPermalink),], debug=True)




