from django.test import TestCase, Client
from ..models import Operator, Mode
from django.contrib.auth.models import User
from ..forms import LoginForm
from django.contrib.auth import authenticate
from django.urls import reverse
from django.shortcuts import render, redirect
from ..views import operator_login, edit_profile


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.admin1 = User.objects.create_user(username='TestAdmin', password='1234', email='test@operator.co.uk.',
                                               first_name='Test Admin')
        self.operator1 = Operator.objects.create(admin=self.admin1, name='TestOperator',
                                                 homepage='https://operator.co.uk',
                                                 api_url='https://test.opentransport.co.uk', phone='07083249084',
                                                 email='test@operator.co.uk')

    def test_operators_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("operator:operators"))
        self.assertRedirects(response, reverse("operator:login"))
        
    def test_edit_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("operator:edit"))
        self.assertRedirects(response, reverse("operator:login"))
        
    def test_login_redirect_if_logged_in(self):
        login = self.client.login(username='TestAdmin', password='1234')
        response = self.client.get(reverse("operator:login"))
        self.assertRedirects(response, reverse("operator:operators"))

    def test_login_response(self):
        response = self.client.post('', {"username": 'TestAdmin', "password": "1234"})
        self.assertEqual(response.status_code, 302)
        
    def test_logout_response(self):
        response = self.client.get(reverse("operator:logout"))
        self.assertRedirects(response, reverse("operator:login"))

class LoginFormTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.admin1 = User.objects.create_user(username='TestAdmin', password='1234', email='test@operator.co.uk.',
                                               first_name='Test Admin')
        self.operator1 = Operator.objects.create(admin=self.admin1, name='TestOperator',
                                                 homepage='https://operator.co.uk',
                                                 api_url='https://test.opentransport.co.uk', phone='07083249084',
                                                 email='test@operator.co.uk')

    def test_loginform_nonexistent_user(self):
        username = "bogus"
        password = "1234"
        
        form = LoginForm(data={"username":username, "password":password})
        self.assertFalse(form.is_valid())
        
        login = self.client.login(username=username, password=password)
        self.assertFalse(login)
        
    def test_loginform_wrong_password(self):
        username = "TestAdmin"
        password = "wrong"
        
        form = LoginForm(data={"username":username, "password":password})
        self.assertFalse(form.is_valid())
        
        login = self.client.login(username=username, password=password)
        self.assertFalse(login)
        
    def test_loginform_correct_details(self):
        username = "TestAdmin"
        password = "1234"
        
        form = LoginForm(data={"username":username, "password":password})
        self.assertTrue(form.is_valid())
        
        login = self.client.login(username=username, password=password)
        self.assertTrue(login)
        
        response = self.client.post(reverse("operator:login"), {"username":username, "password":password})
        self.assertRedirects(response, reverse("operator:operators"))
        
    def test_loginform_cleaned_data(self):
        username = "TestAdmin"
        password = "1234"
        
        form = LoginForm(data={"username":username, "password":password})
        loginName = ""
        loginPass = ""
        if form.is_valid():
            loginName = form.cleaned_data['username']
            loginPass = form.cleaned_data['password']
        self.assertEqual(loginName, username)
        self.assertEqual(loginPass, password)
        
        user = authenticate(username=loginName, password=loginPass)
        self.assertEqual(user, User.objects.get(username=username))
    