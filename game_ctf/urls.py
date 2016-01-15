#
# @author:metastableB
# urls.py
# 
from django.conf.urls import url
from django.shortcuts import render
from . import views
from . import question_views


app_name = 'game_ctf'
urlpatterns = [
	url(r'^$',views.home, name='index'),
	url(r'^home/$',views.home, name='home'),
	url(r'^question/(?P<question_id>[0-9]+)/$',views.question_page, name='question_page'),
	url(r'^submit/(?P<question_id>[0-9]+)/$',views.submit_answer, name='submit_answer'),
	url(r'^leaderboard/$',views.leaderboard,name='leaderboard'),
	url(r'^rules/$',views.rules,name='rules'),

	# TODO :
	# import the url views
	# Custom URL for individual questions 
	url(r'^q_1/',question_views.q_1,name='rules'),
]


