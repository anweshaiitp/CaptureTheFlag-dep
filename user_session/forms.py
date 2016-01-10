#
# @author:metastableB
# forms.py
# 
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms

'''
@metastableB : The inbuild userregistration form was too difficult to modify
	and adapt for our particular case so I decided to user a custom implementation
	by using the code from the actual implementation. This method is an extension
	of django.contrib.auth.UserCreationForm

	Remember that we are using the django.auth module for authentication and team handling.
	The auth module is built to handle users and not teams, and we are hacking around it.

	Handling Forms might not be as straight forward as the guys  at django make it out
	to be. This is how manual form handling is done:
		https://docs.djangoproject.com/en/dev/topics/forms
		Section on rendering forms manually

	NOTE that the form input field CSS values are set in the widget argument whereas the labels
	are set in the html itself
'''

class UserRegistrationForm(forms.ModelForm):
    error_messages = {
        'duplicate_teamname': _("A team with that teamname already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    
    teamname = forms.RegexField(label=_("teamname"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")},
        widget = forms.TextInput(attrs={'class':'form-control form-control-reg', 'placeholder':'Team Name'}))

    password1 = forms.CharField(
    	label=_("password1"),
        widget = forms.PasswordInput(attrs={'class':'form-control form-control-reg', 'placeholder':'Password'}))
    
    password2 = forms.CharField(
    	label=_("Password confirmation"),
        help_text=_("Enter the same password as above, for verification."),
        widget = forms.PasswordInput(attrs={'class':'form-control form-control-reg', 'placeholder':'Re-enter Password'}))
    
    user1 = forms.CharField(
    	required = True,
    	max_length = 30, 
    	min_length = 1, 
    	strip = True,
    	label='user1: AnweshaID',
    	widget=forms.TextInput(attrs={ 'class':'form-control form-control-reg', 'placeholder':'User1: AnweshaID'}))
    
    user2 = forms.CharField(
    	required = True,
    	max_length = 30, 
    	min_length = 1, 
    	strip = True,
    	label='user2: AnweshaID',
    	widget=forms.TextInput(attrs={ 'class':'form-control form-control-reg', 'placeholder':'User2: AnweshaID'}))

    
    user3 = forms.CharField(
    	required = True,
    	max_length = 30, 
    	min_length = 1, 
    	strip = True,
    	label='user3: AnweshaID',
    	widget=forms.TextInput(attrs={ 'class':'form-control form-control-reg', 'placeholder':'User3: AnweshaID'}))

    email = forms.EmailField(
    	required = True,
    	widget=forms.EmailInput(attrs={ 'class':'form-control form-control-reg', 'placeholder':'Contact Email'}))

    college_name = forms.CharField(
    	required = True,
    	max_length = 50, 
    	min_length = 1, 
    	strip = True,
    	widget= forms.TextInput(attrs={'class':'form-control form-control-reg', 'placeholder':'College Name'}))

    mobile_number = forms.RegexField(
    	label=_("Phone Number"), 
    	max_length=10,
        regex=r'^\d{6}$',
        help_text=_("Required. 10 digit mobile number"),
        error_messages={'invalid': _("This value must contain a 10 digit valid mobile number.")},
        widget = forms.TextInput(attrs={'class':'form-control form-control-reg', 'placeholder':'Mobile Number'})
        )
    

    class Meta:
        model = User
        fields = ("teamname","password1", "password2","user1","user2","user3","email","college_name",'mobile_number')

    def clean_teamname(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        teamname = self.cleaned_data["teamname"]
        try:
            User._default_manager.get(username=teamname)
        except User.DoesNotExist:
            return teamname
        raise forms.ValidationError(
            self.error_messages['duplicate_teamname'],
            code='duplicate_teamname',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
'''
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user'''