#
# @author:metastableB
# urls.py
# 
from django.conf.urls import url

from . import views
from .views import template_path

# App names are used for namespacing
app_name = 'user_session'
urlpatterns = [
	#url(r'^.*',views.not_ready,name="not_ready"),
	url(r'^login/',views.login, name='login'),
	url(r'^logout/$',views.logout, name='logout'),
	url(r'^register/$',views.user_registration,name='register'),
	# Placeholders
]


