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
from .settings import QUESTIONS_DIR, info_messages, template_path

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
	if len(question_status_obj.filter(question_status = 'AW')) == 1 :
		messages.add_message(request,
		info_messages['question already solved'][0],info_messages['question already solved'][1])
		return HttpResponseRedirect(reverse('game_ctf:home'))
		
		if request.GET['score'] == '5':
			message = 5
			flag = 'Vendatta'
		else :
			flag = None
			message = '$SCORE'
		return render(request, QUESTIONS_DIR + question.source_file,{'message':message,'flag':flag})
	return HttpResponse("Ouch! Something went wrong. Please return to your home.")

question_urls = { '1' : '/q_1/?score=200' }

##############################################################
	
	content = {'mode' : True}
	if question_id == '3' :
		if request.method == 'GET' and 'generate' in request.GET:
			content = {'generate':True}
		elif request.method == 'GET' and 'name' in request.GET:
			content = {'name':request.GET['name']}
			#Hardcoded answer
			p = re.compile(r'^(.*<\s*img.*src\s*=\s*[\'"].*/static/images/blog/5.jpg[\'"].*>.*)$', re.IGNORECASE)
			if p.match(request.GET['name']):
				content = {'name':request.GET['name'],'solved' : True}	
	
	return render(request, QUESTIONS_DIR + question.source_file,content)

##### QUESTION SPECIFICATIONS #######

'''
QUESTION 1 : Change get request value 
			 define view in question_views
			 change url to redirect 
			 set has_context = 1

QUESTION 9: (hidden)
			Javasceipt redirect 
			Make sure thequestion is not rendered inthe view
			but is present in the database
'''