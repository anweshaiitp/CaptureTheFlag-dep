#
# @author:metastableB
# question_views.py
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
from .settings import QUESTIONS_DIR, info_messages, template_path, question_if_answered
from django.db import connections

import re

question_urls = { '1' : '/q_1/?score=200',
    '3' : '/q_3/',
    '4' : '/q_4/',
    '5' : '/q_5/?story' }


##### QUESTION SPECIFICATIONS #######

'''
QUESTION 1 : Change get request value 
             define view in question_views
             change url to redirect 

QUESTION 9: (hidden)
            Javasceipt redirect 
            Make sure thequestion is not rendered inthe view
            but is present in the database
'''

@login_required
def q_1(request):
    question_id = 1
    if request.method == 'GET' and 'score' in request.GET:
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

    if request.GET['score'] == '5':
        message = 5
        flag = question.answer
    else :
        flag = None
        message = '$SCORE'
    return render(request, QUESTIONS_DIR + question.source_file,{'message':message,'flag':flag})
    return HttpResponse("Ouch! Something went wrong. Please return to your home.")

@login_required
def q_3(request):
    question_id = 3
    try:
        question = Question.objects.filter(valid=True).get(pk = question_id)
    except ObjectDoesNotExist:
        messages.add_message(request, info_messages['question does not exist'][0],
            info_messages['question does not exist'][1])
        return HttpResponseRedirect(reverse('user_session:login'))

    is_answered = question_if_answered(request,question_id,QuestionStatus,question)
    if is_answered is not None:
        return is_answered
    
    content = {'mode' : True}
    if request.method == 'GET' and 'generate' in request.GET:
        content = {'generate':True}
    elif request.method == 'GET' and 'name' in request.GET:
        content = {'name':request.GET['name']}
        #Hardcoded answer
        p = re.compile(r'^(.*<img.*src\s*=\s*[\'"].*/static/images/blog/5.jpg[\'"].*>.*)$', re.IGNORECASE)
        if p.match(request.GET['name']):
            flag = question.answer
            content = {'name':request.GET['name'],'solved' : True,'flag':flag}  
    
    return render(request, QUESTIONS_DIR + question.source_file,content)

@login_required
def q_4(request):
    question_id = 4
    try:
        question = Question.objects.filter(valid=True).get(pk = question_id)
    except ObjectDoesNotExist:
        messages.add_message(request, info_messages['question does not exist'][0],
            info_messages['question does not exist'][1])
        return HttpResponseRedirect(reverse('user_session:login'))

    is_answered = question_if_answered(request,question_id,QuestionStatus,question)
    if is_answered is not None:
        return is_answered
    
    content = {'story' : True}
    if request.method == 'GET' and 'feedback' in request.GET:
        content = {'story':False}
    elif request.method == 'POST' and 'name' in request.POST and 'comment' in request.POST:
        size = len(request.POST['name'])+len(request.POST['comment'])
        msg = "Space Used : "+str(size/1024.0)+" KB"
        if size > 200*1024:
            content = {'solved':True,'msg':msg,'flag':question.answer}
        else:
            content = {'solved':False,'msg':msg}
        
    return render(request, QUESTIONS_DIR + question.source_file,content)
    
@login_required
def q_5(request):
    question_id = 5
    try:
        question = Question.objects.filter(valid=True).get(pk = question_id)
    except ObjectDoesNotExist:
        messages.add_message(request, info_messages['question does not exist'][0],
            info_messages['question does not exist'][1])
        return HttpResponseRedirect(reverse('user_session:login'))

    is_answered = question_if_answered(request,question_id,QuestionStatus,question)
    if is_answered is not None:
        return is_answered

    if request.method == 'GET' and 'story' in request.GET:
        return render(request, QUESTIONS_DIR + question.source_file,{'story':True})

    
    content = {}

    logged_in = False
    name = 'unknown'
    registered = False
    
    ##check cookies
    name = request.COOKIES.get('name')
    if name is not None :
        if name[0]<5 and _name[0]>15 :
            name = None
    login = request.COOKIES.get('login')
    if login and name is not None:
        logged_in = True
        if request.method == 'GET' and 'logout' in request.GET:
            logged_in = False
        
    

    if logged_in == False and request.method == 'POST' and 'name' in request.POST and 'pass' in request.POST and 'pass2' in request.POST:
        content = {'solved':False,'msg':"Registration Failed : Password Didn't Match!",'b_class':'alert alert-warning'}
        if len(request.POST['name'])<5 or len(request.POST['name'])>15:
            content = {'solved':False,'msg':"Invalid Name",'b_class':'alert alert-warning'}
        elif request.POST['name']=='admin':
            content = {'solved':False,'msg':"User Already Registered!",'b_class':'alert alert-warning'}
        elif len(request.POST['pass'])>0 and request.POST['pass']==request.POST['pass2']:
            registered = True
            content = {'solved':False,'registered':True,'msg':"Registration Completed!",'b_class':'alert alert-success'}
    elif logged_in == False and request.method == 'GET' and 'login' in request.GET:
        if name is not None:
            logged_in = True

    if logged_in : 
        content = {'login':name}
        if request.method == 'POST' and 'pass' in request.POST and 'pass_confirm' in request.POST:
            if request.POST['pass']!=request.POST['pass_confirm']:
                    content = {'login':name,'msg':"Password didn't match",'b_class':'alert alert-warning'}
            elif name == 'admin':
                content = {'login':name,'msg':"Admin Password Changed",'b_class':'alert alert-success','solved':True}
            else:
                content = {'login':name,'msg':"CTF : You need to change admin Password",'b_class':'alert alert-warning'}


    response = render(request, QUESTIONS_DIR + question.source_file,content)
    if logged_in:
        response.set_cookie('login','true')
    else:
        response.delete_cookie('login')
        
    if registered:
        response.set_cookie('name',request.POST['name'])
        response.set_cookie('login','false')
    return response
    
    

@login_required
def q_6_404(request):
    question_id = 6
    if request.method == 'GET':
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

    return render(request,template_path['q_6_404'])

@login_required
def q_6_ans(request):
    question_id = 6

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
    if request.method == 'GET':
        return render(request,template_path['q_6_ans'])
    #electronic xxxxxxxx variable automatic computer
    if 'answer' in request.POST:
        if request.POST['answer'] != 'discrete':
            return render(request,template_path['q_6_ans'],{'message':'TRY AGAIN!'})
        else:
            return HttpResponseRedirect(reverse('game_ctf:q_6_')+'?answer=%s'%request.POST['answer']   )
    else:
        messages.add_message(request, info_messages['unknown error'][0],
                info_messages['unknown error'][1])
        return HttpResponseRedirect(reverse('game_ctf:home'))

@login_required
def q_6_(request):
    question_id = 6

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
    if request.method == 'GET' and 'answer' in request.GET and request.GET['answer'] == 'discrete':
        return render(request,template_path['q_6_'])
    if request.method == 'POST':
        row = "DATABASE EXCEPTION : Please Contact administrator."
        try:
            cursor = connections['ctf_sqli'].cursor()
            cursor.execute(request.POST['answer'])
            row = cursor.fetchall()[0][0]
        except Exception as ex:
            pass
        return render(request,template_path['q_6_'],{'message':row})
    else:
        messages.add_message(request, info_messages['unknown error'][0],
                info_messages['unknown error'][1])
        return HttpResponseRedirect(reverse('game_ctf:home'))

    