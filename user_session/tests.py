#
# @author:metastableB
# tests.py
# 
from django.test import TestCase
from django.core.urlresolvers import reverse
from .views import info_messages
from django.contrib.auth.models import User


'''
@metastableB
Tests:
    These tests assume a redirection to `user_session:login'
    * Login with correct credentials when user exists in databse
    * Login with incorrect credentials when user exists in database
    * Login when user does not exist
    * Login with null username and existing userobject
    * Login with null password 
    * Login with inactive user credentials (active to inactive toggle)
    * Login with active user credentials (inactive to active toggle)
    * Login with already authenticated userobject
#TODO :
    [ ] user should not be allowed to visit or do anyting without logging in.
'''


class LoginAttemptsTest(TestCase):

    test_username = 'alrpjrnkldunlaad123'
    test_password='12408ysgnkjhadsgtuyaa'

    def test_login_when_user_exists(self):
        # Should redirect to home with 302 status code
        u = User.objects.create_user(self.test_username,password=self.test_password)
        response = self.client.post(reverse('user_session:login'),
            {'username' : self.test_username,'password' : self.test_password})        
        self.assertRedirects(response,reverse('user_session:home'))

    def test_login_username_password_do_not_match(self):
        u = User.objects.create_user(self.test_username,password = self.test_password)
        response = self.client.post(reverse('user_session:login'), {'username': self.test_username + ('lol') ,'password': self.test_password + ('ls') })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,info_messages['invalid username password'][1])        

    def test_login_when_user_does_not_exist(self):
        response = self.client.post(reverse('user_session:login'), {'username': self.test_username,'password': self.test_password})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,info_messages['invalid username password'][1])

    def test_login_username_is_null(self):
        u = User.objects.create_user(self.test_username, password = self.test_password)
        response = self.client.post(reverse('user_session:login'),{'username':'','password':self.test_password})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,info_messages['invalid username password'][1])

    def test_login_username_is_null(self):
        u = User.objects.create_user(self.test_username, password = self.test_password)
        response = self.client.post(reverse('user_session:login'),{'username':self.test_username,'password':''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,info_messages['invalid username password'][1])

    def test_login_user_toggeld_to_inactive(self):
        u = User.objects.create_user(self.test_username, password = self.test_password)
        response = self.client.post(reverse('user_session:login'),
            {'username' : self.test_username, 'password' : self.test_password})
        self.assertRedirects(response,reverse('user_session:home'))
        self.client.get(reverse('user_session:logout'))

        u.is_active = False
        u.save()
        response = self.client.post(reverse('user_session:login'),
            {'username' : self.test_username, 'password' : self.test_password})        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,info_messages['invalid username password'][1])

    def test_login_user_toggled_to_active(self):
        u = User.objects.create_user(self.test_username, password = self.test_password)
        u.is_active = False
        u.save()
        response = self.client.post(reverse('user_session:login'),
            {'username' : self.test_username, 'password' : self.test_password})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,info_messages['invalid username password'][1])        

        u.is_active = True
        u.save()
        response = self.client.post(reverse('user_session:login'),
            {'username' : self.test_username, 'password' : self.test_password})
        self.assertRedirects(response,reverse('user_session:home'))
        self.client.get(reverse('user_session:logout'))


    def test_login_user_already_authenticated(self):
        u = User.objects.create_user(self.test_username, password = self.test_password)
        response = self.client.post(reverse('user_session:login'),
            {'username' : self.test_username, 'password' : self.test_password})

        response = self.client.get(reverse('user_session:login'))
        self.assertRedirects(response,reverse('user_session:home'))



'''
Tests:
    For now we have not modified django.contrib.auth.form.UserRegistrationForm
    and can rely on its robustness. In the event that we extend the calls,
    we will have to write test cases.
'''


class RegistrationAttemptsTest(TestCase):
    pass