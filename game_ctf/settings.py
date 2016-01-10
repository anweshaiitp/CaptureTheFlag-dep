#
# @author:metastableB
# settings.py
# 
from django.contrib import messages
'''
@metastableB : where the question files will be searched for.
	Refer to views.question_page for usage.
	Should be a top level sub directory of templates/ . If you need
	to modify the direcory structure, add the new directory to the 
	global settings.TEMPLATE
'''
QUESTIONS_DIR='testQuestions/'

info_messages = {
	'normal user page':(messages.INFO,'Logged Out: Game Not For Admin'),
	'question does not exist' :(messages.ERROR,'Does Not Exist: Seriously dude ?'),
	'question already solved' :(messages.INFO,'Already Soved : Why Solve Again??'),
	'login required':(messages.INFO,'You must login first'),
}

template_path = {
	'home':'game_ctf/home.html',
	'leaderboard':'game_ctf/leaderboard.html',
	'rules' : 'game_ctf/rules.html'
}	