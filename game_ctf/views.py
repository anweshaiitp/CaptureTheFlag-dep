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
from models import Question
@login_required 
def home(request):
	questions = Question.objects.all().filter(valid=True)
	return render(request, 'game_ctf/home.html',{'questions':questions})


@login_required
def question_page(request,question_id):
	try:
		question = Question.objects.get(pk = question_id)
	except ObjectDoesNotExist:
		# TODO: WTF ???
		# return him to home with some funny message
		pass
	# TODO :check question status and verify that it is not solved
	# then go back to home 
	return render(request,'testQuestions/' + question.source_file)

@login_required 
def leaderboard(request):
	return HttpResponse("Apparently you are winning")