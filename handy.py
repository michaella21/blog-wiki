
import hmac
import hashlib
from string import letters
import hmac
import hashlib
import random
import re
from string import letters


"""
#helper function to make import file from other directory easier
def load_src(name, fpath):
	import os, imp
	return imp.load_source(name, os.path.join(os.path.dirname(__file__), fpath))
"""

secret = "mittens"
#Password stored as 5-character salt + shat256
def make_salt(length = 5):
	return ''.join(random.choice(letters) for i in range(length))

def make_pw_hash(name, pw, salt=None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(str(name) + str(pw) + str(salt)).hexdigest()
	return '%s,%s' %(h, salt)

def valid_pw(name, pw, h):
	salt = h.split(',')[1]
	return h == make_pw_hash(name, pw, salt)

#Cookies stored as cookie_name = make_secure_val(val)
def make_secure_val(val):
	return "%s|%s" % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
	val = secure_val.split('|')[0]
	if make_secure_val(val) == secure_val:
		return val

#Regular expressions: check the vaildity of user inputs
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

def valid_username(username):
	return username and USER_RE.match(username)

def valid_password(password):
	return password and PASS_RE.match(password)

def valid_email(email):
	return not email or EMAIL_RE.match(email)

