#
# @author:metastableB
# admin.py
# 
from django.contrib import admin
from models import Question, TeamMembers, QuestionStatus

admin.site.register(Question)
admin.site.register(QuestionStatus)
admin.site.register(TeamMembers)
