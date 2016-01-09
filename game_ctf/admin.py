#
# @author:metastableB
# admin.py
# 
from django.contrib import admin
from models import Question, Team, QuestionStatus

admin.site.register(Question)
admin.site.register(Team)
admin.site.register(QuestionStatus)