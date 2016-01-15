#
# @author:metastableB
# forms.py
# 
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms

from game_ctf.models import TeamDetail, People

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
        'anw_same_id': _("Two Users Can't Have Same ANW ID"),
        'anw_exists': _("User Already Registered "),
        'anw_not_found': _("Arey you registered with anwesha 16? AnweshaID not found:")
    }
    
    teamname = forms.RegexField(
    	required=True,
    	label=_("teamname"), 
    	max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")},
        widget = forms.TextInput(attrs={'class':'form-control form-control-reg', 'placeholder':'Team Name'}))

    password1 = forms.CharField(
    	label=_("password1"),
        widget = forms.PasswordInput(attrs={'class':'form-control form-control-reg', 'placeholder':'Password'}))
    
    password2 = forms.CharField(
    	label=_("Password confirmation"),
        help_text=_("Enter the same password as above, for verification."),
        widget = forms.PasswordInput(attrs={'class':'form-control form-control-reg', 'placeholder':'Re-enter Password'}))
    
    user1 = forms.RegexField(
    	required = True,
    	min_length = 1, 
    	label='user1: AnweshaID',
    	max_length=10,
        regex=r'^[Aa][Nn][Ww]\d{4}$',
        error_messages={'invalid': _("Enter a valid anweshaID")},
    	widget=forms.TextInput(attrs={ 'class':'form-control form-control-reg', 'placeholder':'User1: AnweshaID'}))
    
    user2 = forms.RegexField(
    	required = True,
    	min_length = 1, 
    	label='user2: AnweshaID',
    	max_length=10,
        regex=r'^[Aa][Nn][Ww]\d{4}$',
        error_messages={'invalid': _("Enter a valid anweshaID")},
    	widget=forms.TextInput(attrs={ 'class':'form-control form-control-reg', 'placeholder':'User2: AnweshaID'}))
    
    user3 = forms.RegexField(
    	required = True,
    	min_length = 1, 
    	label='user3: AnweshaID',
    	max_length=10,
        regex=r'^[Aa][Nn][Ww]\d{4}$',
        error_messages={'invalid': _("Enter a valid anweshaID")},
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
        regex=r'^\d{10}$',
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

    def clean_user3(self):
        u = [self.cleaned_data['user1'].upper(),self.cleaned_data['user2'].upper(),self.cleaned_data['user3'].upper() ]
        for i in [0,1,2]:
            for j in [0,1,2]:
                if i!=j:
                    if u[i] == u[j]:
                        raise forms.ValidationError(
                            self.error_messages['anw_same_id'],
                            code='anw_same_id',
                        )

        for i in [0,1,2]:
            forUser1 = TeamDetail.objects.filter(user1 = u[i]);
            forUser2 = TeamDetail.objects.filter(user2 = u[i]);
            forUser3 = TeamDetail.objects.filter(user3 = u[i]);
            if len(forUser1)+len(forUser2)+len(forUser3) != 0 :
                #user already exists
                raise forms.ValidationError(
                            self.error_messages['anw_exists'] + u[i],
                            code='anw_exists',
                        )
        for i in [0,1,2]:
            try:
                a_user1 = People.objects.using('anwesha').get(pid=u[i][3:])
            except People.DoesNotExist:
                raise forms.ValidationError(
                        self.error_messages['anw_not_found'] +u[i],
                        code='anw_not_found')

        return self.cleaned_data.get("user3")
        
'''
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user'''