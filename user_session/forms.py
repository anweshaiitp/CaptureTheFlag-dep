#
# @author:metastableB
# forms.py
# 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
# Extending the form.
# http://jessenoller.com/blog/2011/12/19/quick-example-of-extending-usercreationform-in-django

class UserRegistrationForm(UserCreationForm):
    user1 = forms.CharField(required = True,max_length = 30, min_length = 1, strip = True)
    user2 = forms.CharField(required = True,max_length = 30, min_length = 1, strip = True)
    user3 = forms.CharField(required = True,max_length = 30, min_length = 1, strip = True)
    college_name = forms.CharField(required = True,max_length = 30, min_length = 1, strip = True)
    phone_number = forms.IntegerField(required = True)
    email = forms.EmailField(required = True)

    class Meta:
        model = User
        fields = ("username","email","user1","user2","user3","password1", "password2","phone_number","college_name")
