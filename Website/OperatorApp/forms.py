from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Mode, Operator

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-group'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-group'}))

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


class OperatorForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : 'form-group'}))
    modes = forms.ModelMultipleChoiceField(
        queryset=Mode.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class' : 'form-group'}),
    )
    homepage = forms.URLField(required=False, widget=forms.TextInput(attrs={'class' : 'form-group'}))
    api_url = forms.URLField(required=False, widget=forms.TextInput(attrs={'class' : 'form-group'}))
    default_language = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : 'form-group'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : 'form-group'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class' : 'form-group'}))
    active = forms.BooleanField(required=False)

    class Meta:
        model = Operator
        fields = ['name', 'modes', 'homepage', 'api_url', 'default_language', 'phone', 'email', 'active']