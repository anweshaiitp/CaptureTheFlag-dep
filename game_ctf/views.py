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

from models import Question, QuestionStatus, TeamDetail
from .settings import QUESTIONS_DIR, info_messages, template_path

@login_required 
def home(request):
	questions = Question.objects.all().filter(valid=True)
	try:
		score = TeamDetail.objects.get(team = request.user).points
	except ObjectDoesNotExist:
		messages.add_message(request,
		info_messages['normal user page'][0],info_messages['normal user page'][1])
		return HttpResponseRedirect(reverse('user_session:logout'))

	team_name = request.user.username
	return render(request, template_path['home'],{'questions':questions, 'score':score, 'team_name' :team_name})


@login_required
def submit_answer(request,question_id):
	try:
		question = Question.objects.get(pk = question_id)
		if request.method == 'GET' and 'answer' in request.GET:
			answer = request.GET['answer']
			if question.answer == answer:
				qs = QuestionStatus(
					team_id = request.user,
					question_id = question,
					question_status = 'AW')
				qs.save()
				return HttpResponse("wow")
			else:
				return HttpResponse("tryagain")
			return HttpResponse("error2")

	except ObjectDoesNotExist:
		pass
	return HttpResponse("error")


@login_required
def question_page(request,question_id):
	try:
		question = Question.objects.get(pk = question_id)
	except ObjectDoesNotExist:
		messages.add_message(request,
			info_messages['question does not exist'][0],info_messages['question does not exist'][1])
	question_status_obj = QuestionStatus.objects.filter(team_id = request.user).filter(question_id = question).filter(question_status = 'AW')	
	if len(question_status_obj) == 1 :
		messages.add_message(request,
		info_messages['question already solved'][0],info_messages['question already solved'][1])
		return HttpResponseRedirect(reverse('game_ctf:home'))

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
