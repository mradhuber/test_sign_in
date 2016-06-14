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
#
import webapp2
import cgi
import re

form="""<form method = "post">
        <b>SIGN IN:</b>
        <br>
   			<label> Username 
   				<input type = "text" name = "username" value = "%(username)s">
   				%(uname_error)s
   			</label>
   			<br>
   			<label> Password 
   				<input type = "password" name = "password">
   				%(pword_error)s
   			</label>
   			<br>
   			<label> Verify Password
   				<input type = "password" name = "verify">
   				%(verify_error)s
   			</label>
   			<br>
   			<label> Email (optional) 
   				<input type = "text" name = "email" value = "%(email)s">
   				%(email_error)s
   			</label>
	<br><br>
	<input type="submit">
</form>"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def check_username(username):
	return USER_RE.match(username)

def check_password(password):
	return PWORD_RE.match(password)

def check_verify(verify, password):
	return verify == password

def check_email(email):

	if email == "" or EMAIL_RE.match(email):
		return True
	
	return False

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.write_form()

    def post(self):
		username_in = self.request.get('username')
		password_in = self.request.get('password')
		verify_in = self.request.get('verify')
		email_in = self.request.get('email')

		c_uname = check_username(username_in)
		c_pword = check_password(password_in)
		c_verify = check_verify(verify_in, password_in)
		c_email = check_email(email_in)

		uname_err = ""
		pword_err = ""
		verify_err = ""
		email_err = ""

		if not c_uname:
			uname_err = "Please enter a valid username."
		if not c_pword:
			pword_err = "Please enter a valid password."
		if not c_verify:
			if c_pword:
				verify_err = "Passwords do not match. Try again."
		if not c_email:
			email_err = "Please enter a valid email."

		if (c_uname and c_email and c_verify and c_pword):
			self.redirect('/welcome')
		else:
			self.write_form(username_in, email_in, uname_err, 
				pword_err, verify_err, email_err)

    def write_form(self, username = "", email = "", uname_error = "", pword_error = "", 
    	verify_error = "", email_error = ""):
    	self.response.out.write(form % {"username": username, "email": email,
    	 "uname_error": uname_error, "pword_error": pword_error,
    	 "verify_error": verify_error, "email_error": email_error})

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('Welcome!')

app = webapp2.WSGIApplication([('/', MainHandler), ('/welcome', WelcomeHandler)], debug=True)