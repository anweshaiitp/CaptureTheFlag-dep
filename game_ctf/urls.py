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
	url(r'^contact/$',views.contact,name='contact'),

	# TODO :
	# import the url views
	# Custom URL for individual questions 
	url(r'^q_1/',question_views.q_1,name='q_1'),
	url(r'^q_3/',question_views.q_3,name='q_3'),
	url(r'^q_4/',question_views.q_4,name='q_4'),
	url(r'^q_5/',question_views.q_5,name='q_5'),

	## Url for question 6
	url(r'^404_frost/',question_views.q_6_404,name='q_6_404'),
	url(r'^ans_frost/',question_views.q_6_ans,name='q_6_ans'),
	url(r'^_frost/',question_views.q_6_,name='q_6_'),
]


