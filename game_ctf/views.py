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

@login_required 
def home(request):
	return HttpResponse("Hello Home")


@login_required
def question_page(request):
	return HttpResponse("question page")

@login_required 
def leaderboard(request):
	return HttpResponse("Apparently you are winning")