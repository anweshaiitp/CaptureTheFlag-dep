#
# @author:metastableB
# settings.py
# 
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
'''
@metastableB : where the question files will be searched for.
	Refer to views.question_page for usage.
	Should be a top level sub directory of templates/ . If you need
	to modify the direcory structure, add the new directory to the 
	global settings.TEMPLATE
'''
QUESTIONS_DIR='questions/'

# Some messages are hardcoded into the home.html javascript and used for comparison
info_messages = {
	'normal user page':(messages.INFO,'Logged Out: Game Not For Admin'),
	'question does not exist' :(messages.ERROR,'Does Not Exist: Seriously dude ?'),
	'invalid_request' :(messages.ERROR,'Invalid Request'),
	'question already solved' :(messages.INFO,'Already Soved : Why Solve Again??'),
	'login required':(messages.INFO,'You must login first'),
	'invalid_question':(messages.ERROR,"InvalidQuestion"),
	'answered':(messages.INFO,"AlreadySubmmited"),
	'correct answer':(messages.INFO,"CrackedIt"),
	'incorrect answer':(messages.INFO,"InvalidFlag"),
	'unknown error':(messages.INFO,"unknown error"),
}

template_path = {
	'home':'game_ctf/home.html',
	'leaderboard':'game_ctf/leaderboard.html',
	'rules' : 'game_ctf/rules.html',
	'contact' : 'game_ctf/contact.html',
	
	# Question templates:
	'q_6_404' : 'questions/sqli_frost_404.html',
	'q_6_ans' : 'questions/sqli_frost_ans.html',
	'q_6_': 'questions/sqli_frost_sqli.html',
}	

def question_if_answered(request,question_id,QuestionStatus,question):
	question_status_obj = QuestionStatus.objects.filter(team_id = request.user).filter(question_id = question)
	if len(question_status_obj.filter(question_status = 'AW')) == 1 :
		messages.add_message(request,
		info_messages['question already solved'][0],info_messages['question already solved'][1])
		return HttpResponseRedirect(reverse('game_ctf:home'))
	return None
