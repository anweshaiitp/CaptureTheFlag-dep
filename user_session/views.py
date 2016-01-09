#
# @author:metastableB
# views.py
# 
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.views import logout as auth_logout
from django.contrib.auth.views import login as auth_login
from django.contrib import messages
from django.core.urlresolvers import resolve, Resolver404, is_valid_path
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm
from .settings import template_path, info_messages
from game_ctf.models import TeamMembers

from django.contrib.auth.models import User
import settings 

'''
@metastableB : The page to redirect to if  `next` is not given or is empty.
	If this is left to None we default to dango's settings.LOGIN_REDIRECT_URL
	used by django.contrib.auth module
'''
redirect_to_url = settings.LOGIN_REDIRECT_URL

'''
@metastableB : From the docs
	If called via GET, it displays a login form that POSTs to the same URL.
	If called via POST with user submitted credentials, it tries to log the user in.
	If login is successful, the view redirects to the URL specified in next. 
	If next isn't provided, it redirects to settings.LOGIN_REDIRECT_URL.
'''

@login_required
def home(request):
	return render(request, template_path['home'], {'user' : request.user})

def login(request):
	next_ = None
	if request.method == 'GET' and 'next' in request.GET:
		next_ = request.GET['next']
		if not is_valid_path(next_):
			next_ = None

	if request.user.is_authenticated():
		if next_ == None:
			return HttpResponseRedirect(reverse(redirect_to_url))
		else:
			return HttpResponseRedirect(next_)

	if next_ != None:
		messages.add_message(request,
			info_messages['login required'][0],info_messages['login required'][1])
	return auth_login(request,template_name = template_path['login'])

def logout(request):
	user = request.user
	if user.is_authenticated():
			messages.add_message(request,
				info_messages['logged out'][0],info_messages['logged out'][1])
	return auth_logout(request,next_page=reverse('user_session:login'))

def save_team(registration_form):
	'''
	* user1
	* user2
	* user3
	* username (TeamName)
	* password1
	* email 
	* college_name
	* phone_number
	'''
	u = User.objects.create_user(registration_form.cleaned_data['username'],
		password = registration_form.cleaned_data['password1'])
	team = TeamMembers(team = u,
		email = registration_form.cleaned_data['email'],
		user1 = registration_form.cleaned_data['user1'],
		user2 = registration_form.cleaned_data['user2'],
		user3 = registration_form.cleaned_data['user3'],
		college_name = registration_form.cleaned_data['college_name'],
		phone_number = registration_form.cleaned_data['phone_number'])
	team.save()
	

def user_registration(request):
	user = request.user
	if user.is_authenticated():
		# TODO: Make this into a pop up message on the same page
		messages.add_message(request,
			info_messages['logout first'][0],info_messages['logout first'][1])
		return HttpResponseRedirect(reverse(redirect_to_url	))
	if request.method == 'POST':
		registration_form = UserRegistrationForm(request.POST)
		if registration_form.is_valid():
			#print registration_form.cleaned_data
			messages.add_message(request,
			info_messages['registration successful'][0],info_messages['registration successful'][1])
			save_team(registration_form)
			return HttpResponseRedirect(reverse('user_session:login'))
	else:
			registration_form = UserRegistrationForm()

	return render(request, template_path['registration'], {'form' : registration_form})