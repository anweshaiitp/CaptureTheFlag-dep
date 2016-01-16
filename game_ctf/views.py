#
# @author:metastableB
# views.py
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
from datetime import datetime
from django.utils import timezone

from models import Question, QuestionStatus, TeamDetail, Log
from .settings import QUESTIONS_DIR, info_messages, template_path, question_if_answered
from .question_views import question_urls

def not_ready(request):
	render(request,template_path['not_ready'])

@login_required 
def home(request):
	questions = Question.objects.all().filter(valid=True).exclude(hidden = True)
	try:
		score = TeamDetail.objects.get(team = request.user).points
	except ObjectDoesNotExist:
		messages.add_message(request,
		info_messages['normal user page'][0],info_messages['normal user page'][1])
		return HttpResponseRedirect(reverse('user_session:logout'))

	team_name = request.user.username
	_questions = []
	for ques in questions:
		question_status_obj = QuestionStatus.objects.filter(team_id = request.user).filter(question_id = ques).filter(question_status = 'AW')	
		if len(question_status_obj) == 1 :
			_questions.append( ( ques.pk,True,ques.points) )	#Solved
		else:
			_questions.append( ( ques.pk,False,ques.points) )	#Unsolved

	if len(_questions) == 0:
		HttpResponse("Database Error")
	return render(request, template_path['home'],{'shortteamname':team_name[:5],'questions':_questions, 'score':score, 'team_name' :team_name,})


@login_required
def submit_answer(request,question_id):
	if request.method == 'POST' and 'answer' in request.POST:
		try:
			question = Question.objects.filter(valid=True).get(pk = question_id)
		except ObjectDoesNotExist:
				return HttpResponse(info_messages['invalid_question'][1])
		question_status_obj = QuestionStatus.objects.filter(team_id = request.user).filter(question_id = question)
		#Question Already Answered
		if len(question_status_obj.filter(question_status = 'AW')) !=0 :
			return HttpResponse(info_messages['answered'][1])
			
		_log = Log.objects.filter(team_id = request.user).filter(question_id = question)
		if len(_log) == 0 :
			log = Log(team_id = request.user,
				question_id = question,
				)
		else:
			log = _log[0]
		log.submission_time = timezone.now()
			
		#Question Already Opened
		if len(question_status_obj) !=0 :
			qs = question_status_obj[0]
		else:
			qs = QuestionStatus(
				team_id = request.user,
				question_id = question,
				question_status = 'OP')
			
		answer = request.POST['answer']
		if question.answer == answer:
			log.solved = True
			qs.question_status = 'AW'
			qs.submission_time = timezone.now()
			qs.save()
			team = TeamDetail.objects.filter(team = qs.team_id)[0];
			team.points+=qs.question_id.points;
			team.save()
			log.save()
			return HttpResponse(info_messages['correct answer'][1])
		else:
			log.count_fail += 1
			qs.submission_time = timezone.now()
			qs.save()
			log.save()
			return HttpResponse(info_messages['incorrect answer'][1])
	return HttpResponse(info_messages['invalid_request'][1])


@login_required
def question_page(request,question_id):
	try:
		question = Question.objects.filter(valid=True).get(pk = question_id)
	except ObjectDoesNotExist:
		messages.add_message(request, info_messages['question does not exist'][0],
			info_messages['question does not exist'][1])
		return HttpResponseRedirect(reverse('user_session:login'))

	question_status_obj = QuestionStatus.objects.filter(team_id = request.user).filter(question_id = question)
	is_answered = question_if_answered(request,question_id,QuestionStatus,question)
	if is_answered is not None:
		return is_answered
	
	#Question not opened
	if len(question_status_obj) ==0 :
		qs = QuestionStatus(
			team_id = request.user,
			question_id = question,
			question_status = 'OP')
		qs.save()

	if question.has_context:
		return HttpResponseRedirect(question_urls[question_id])
	
	return render(request, QUESTIONS_DIR + question.source_file)


def leaderboard(request):
	template = loader.get_template('game_ctf/leaderboard.html')
	rlist_ = TeamDetail.objects.all().order_by('-points')[:20];
	rlist = []
	rank = 1
	for row in rlist_:
		rlist.append( ( rank,row.team.username,row.points) )
		rank+=1
	content = { 
		'ranklist' : rlist	
	}
	return render(request, template_path['leaderboard'],content)

def rules(request):
	return render(request, template_path['rules'])

def contact(request):
	return render(request, template_path['contact'])
