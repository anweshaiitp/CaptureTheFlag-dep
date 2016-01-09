#
# @author:metastableB
# urls.py
# 
from django.conf.urls import url
from . import views

app_name = 'game_ctf'
urlpatterns = [
	url(r'^$',views.home, name='index'),
	url(r'^home/',views.home, name='home'),
	url(r'^question/(?P<question_id>[0-9]+)/$',views.question_page, name='question_page'),
	url(r'^leaderboard/$',views.leaderboard,name='leaderboard'),
	# Placeholders
]


