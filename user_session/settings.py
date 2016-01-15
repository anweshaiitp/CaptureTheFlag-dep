#
# @author:metastableB
# settings.py
# 
from django.contrib import messages
"""
@metastableB
These are settings for the django.contrib.auth module.
We have overridden them with our specifics.
Refer the documentation for more details.
"""
LOGIN_REDIRECT_URL = 'game_ctf:home'
LOGIN_URL = 'user_session:login'
LOGOUT_URL = 'user_session:error_404'

# Different template paths stored as a dictonary
template_path = {
	'login':'user_session/login_logout.html',
	'registration' : 'user_session/register.html',
	'home' :'user_session/home.html',
	'not_ready' : 'user_session/not_ready.html'
}
# Info messages used across module
info_messages = {
	'login required':(messages.INFO,'You must login first'),
	'logged out':(messages.INFO, 'You have successfully logged out.'),
	'logout first' : (messages.INFO, "Sorry, you need to logout first."),
	'registration successful' : (messages.INFO, 'Registration successful, please login to continue.'),
	'invalid username password':(messages.ERROR,"Sorry, that's not a valid username or password"),
	'reg_failed':(messages.ERROR,"Registration Failed : "),
	'redirect_to_url not set' : (messages.ERROR, "ERROR: redirect_to_url not set in user_session:views"),
}
