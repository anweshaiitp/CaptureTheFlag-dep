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
    first_name = forms.CharField(required = True,max_length = 30, min_length = 1, strip = True)
    last_name = forms.CharField(required = True,max_length = 30, min_length = 1, strip = True)
    email = forms.EmailField(required = True)
    class Meta:
        model = User
        fields = ("first_name","last_name","username", "email", "password1", "password2")
