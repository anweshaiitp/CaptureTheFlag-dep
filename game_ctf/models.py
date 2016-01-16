#
# @author:metastableB
# models.py
# 
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User 
from django import forms
from django.utils import timezone
from datetime import timedelta

from CaptureTheFlag.settings import BASE_DIR

class Question(models.Model):
	valid = models.BooleanField(default = True)
	hidden = models.BooleanField(default = False)
	source_file = models.CharField(max_length=50)
	answer = models.CharField(max_length=50)
	points = models.IntegerField(default = 0)
	# Some questions will require additional context information
	# such as specific rendering of modification requests, if this is
	# the case we will have to handle such questions separately 
	has_context = models.BooleanField(default = True)
	def __str__(self):
		return str(self.pk) + " " + self.source_file

class TeamDetail(models.Model):
	# TODO : enforce validators
	team = models.ForeignKey(User,on_delete = models.CASCADE)
	non_competing = models.BooleanField(default=False)
	valid = models.BooleanField(default = True)
	user1 = models.CharField(max_length = 30)
	user2 = models.CharField(max_length = 30)
	user3 = models.CharField(max_length = 30)
	email = models.EmailField()
	college_name = models.CharField(max_length = 30)
	phone_number = models.CharField(max_length = 15)
	points = models.IntegerField(default = 0)
	def __str__(self):
		return str(self.team.pk) + " : " + self.team.username 

'''
@metastableB : We are not using a leaderboard specific data structure for this app
	Our assumption is that the number of users will always remain under, say 1000.
	This means we can afford to query this table, and sort the users according to
	the points alloted to populate the leaderboard.

	In case the number of users gets significant or this querying gets slow, we will
	have to resort to a better LeaderBoard ranking system and scheme, like the ones
	followed by steam/counter_strike/SO etc
'''
class QuestionStatus(models.Model):
	team_id = models.ForeignKey(User,on_delete = models.CASCADE)
	question_id = models.ForeignKey(Question,on_delete = models.PROTECT)
	submission_time = models.DateTimeField(auto_now_add=True)
	open_time = models.DateTimeField(auto_now_add=True)
        
	OPEN = 'OP'
	CLOSED = 'CL'
	ANSWERED = 'AW'
	QUESTION_STATUS_CHOICES = ((OPEN,"Open"),
		(CLOSED,"Closed"),
		(ANSWERED,"Answered"))
	question_status = models.CharField(max_length = 2, choices = QUESTION_STATUS_CHOICES, default = CLOSED)
	def __str__(self):
		return  self.team_id.username+" "+str(self.question_id.pk)+". "+self.question_id.source_file+"("+str(self.question_id.points)+")  Time : "+str((self.open_time+ timedelta(hours=5,minutes=30)).strftime('%l:%M%p'))+" to "+str((self.submission_time+ timedelta(hours=5,minutes=30)).strftime('%l:%M%p'))

class Log(models.Model):
	team_id = models.ForeignKey(User,on_delete = models.CASCADE)
	question_id = models.ForeignKey(Question,on_delete = models.PROTECT)
	count_fail = models.IntegerField(default=0)
	solved = models.BooleanField(default = False)
	submission_time = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		msg = self.team_id.username+" "+str(self.question_id.pk)+". "+self.question_id.source_file+"  "+str((self.submission_time+ timedelta(hours=5,minutes=30)).strftime('%l:%M%p'))
		if self.solved :
			msg+=" (SOLVED) "
		else:
			msg+=" (unsolved) "
		return msg

'''
The anweshd peoples database;
This is used to link to the anwesha table.
We only have read access to that DB.
'''
'''
class People(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    pid = models.IntegerField(db_column='pId', primary_key=True)  # Field name made lowercase.
    college = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    mobile = models.CharField(unique=True, max_length=13, blank=True, null=True)
    email = models.CharField(unique=True, max_length=60, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    feepaid = models.IntegerField(db_column='feePaid', blank=True, null=True)  # Field name made lowercase.
    confirm = models.IntegerField()
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'People'
'''
'''
Dabaase model for SQLI
Make sure the databse is separate from the default and that
the user does not have any privillages except select
'''
class Flags(models.Model):
    flag = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flags'


	