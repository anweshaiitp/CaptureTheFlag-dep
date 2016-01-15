#
# @author:metastableB
# question_views.py
# 

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.urlresolvers import resolve, Resolver404, is_valid_path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from django.template import loader

from models import Question, QuestionStatus, TeamDetail
from .settings import QUESTIONS_DIR, info_messages, template_path, question_if_answered

import re

question_urls = { '1' : '/q_1/?score=200',
	'3' : '/q_3/',
	'4' : '/q_4/',
	'5' : '/q_5/' }


##### QUESTION SPECIFICATIONS #######

'''
QUESTION 1 : Change get request value 
			 define view in question_views
			 change url to redirect 

QUESTION 9: (hidden)
			Javasceipt redirect 
			Make sure thequestion is not rendered inthe view
			but is present in the database
'''

@login_required
def q_1(request):
	question_id = 1
	if request.method == 'GET' and 'score' in request.GET:
		try:
			question = Question.objects.get(pk = question_id)
		except ObjectDoesNotExist:
			messages.add_message(request, info_messages['question does not exist'][0],
				info_messages['question does not exist'][1])
			return HttpResponseRedirect(reverse('user_session:login'))

	question_status_obj = QuestionStatus.objects.filter(team_id = request.user).filter(question_id = question)
	is_answered = question_if_answered(request,question_id,QuestionStatus,question)
	if is_answered is not None:
		return is_answered
	
###################		NEED TO CHECK id score Exists
	if request.GET['score'] == '5':
		message = 5
		flag = 'Vendatta'
	else :
		flag = None
		message = '$SCORE'
	return render(request, QUESTIONS_DIR + question.source_file,{'message':message,'flag':flag})
	return HttpResponse("Ouch! Something went wrong. Please return to your home.")

@login_required
def q_3(request):
	question_id = 3
	try:
		question = Question.objects.get(pk = question_id)
	except ObjectDoesNotExist:
		messages.add_message(request, info_messages['question does not exist'][0],
			info_messages['question does not exist'][1])
		return HttpResponseRedirect(reverse('user_session:login'))

	is_answered = question_if_answered(request,question_id,QuestionStatus,question)
	if is_answered is not None:
		return is_answered
	
	content = {'mode' : True}
	if request.method == 'GET' and 'generate' in request.GET:
		content = {'generate':True}
	elif request.method == 'GET' and 'name' in request.GET:
		content = {'name':request.GET['name']}
		#Hardcoded answer
		p = re.compile(r'^(.*<img.*src\s*=\s*[\'"].*/static/images/blog/5.jpg[\'"].*>.*)$', re.IGNORECASE)
		if p.match(request.GET['name']):
			content = {'name':request.GET['name'],'solved' : True}	
	
	return render(request, QUESTIONS_DIR + question.source_file,content)

@login_required
def q_4(request):
	question_id = 4
	try:
		question = Question.objects.get(pk = question_id)
	except ObjectDoesNotExist:
		messages.add_message(request, info_messages['question does not exist'][0],
			info_messages['question does not exist'][1])
		return HttpResponseRedirect(reverse('user_session:login'))

	is_answered = question_if_answered(request,question_id,QuestionStatus,question)
	if is_answered is not None:
		return is_answered
	
	content = {'story' : True}
	if request.method == 'GET' and 'feedback' in request.GET:
		content = {'story':False}
	elif request.method == 'POST' and 'name' in request.POST and 'comment' in request.POST:
		size = len(request.POST['name'])+len(request.POST['comment'])
		msg = "Space Used : "+str(size/1024.0)+" KB"
		if size > 200*1024:
			content = {'solved':True,'msg':msg}
		else:
			content = {'solved':False,'msg':msg}
		
	return render(request, QUESTIONS_DIR + question.source_file,content)
	
@login_required
def q_5(request):
	question_id = 5
	try:
		question = Question.objects.get(pk = question_id)
	except ObjectDoesNotExist:
		messages.add_message(request, info_messages['question does not exist'][0],
			info_messages['question does not exist'][1])
		return HttpResponseRedirect(reverse('user_session:login'))

	is_answered = question_if_answered(request,question_id,QuestionStatus,question)
	if is_answered is not None:
		return is_answered
	content = {}
	if request.method == 'POST' and 'pass' in request.POST and 'pass2' in request.POST:
		content = {'solved':False,'msg':"Registration Failed : Password Didn't Match!",'b_class':'alert alert-warning'}
		if len(request.POST['pass'])>0 and request.POST['pass']==request.POST['pass2']:
			content = {'solved':True,'msg':"Registration Completed!",'b_class':'alert alert-success'}
		
	return render(request, QUESTIONS_DIR + question.source_file,content)
	
	

