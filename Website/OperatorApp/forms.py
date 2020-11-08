from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        user_name = self.cleaned_data['username']
        pw = self.cleaned_data['password']

        # check the user exists
        if not User.objects.filter(username=user_name).exists():
            raise forms.ValidationError("This user does not exist.")
        
        # check user's authentication details are correct
        if not authenticate(username=user_name, password=pw):
            raise forms.ValidationError("Invalid login details.")

        return self.cleaned_data