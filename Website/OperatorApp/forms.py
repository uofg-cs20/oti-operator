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
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), disabled=True)
    modes = forms.ModelMultipleChoiceField(
        queryset=Mode.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'id':'modes'}),
    )
    homepage = forms.URLField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    api_url = forms.URLField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    miptaurl = forms.URLField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    default_language = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    active = forms.BooleanField(required=False)

    class Meta:
        model = Operator
        fields = ['name', 'modes', 'homepage', 'api_url', 'miptaurl', 'default_language', 'phone', 'email', 'active']
        
        
class RegisterForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    operator_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    modes = forms.ModelMultipleChoiceField(
        queryset=Mode.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'id':'modes'}),
    )
    homepage = forms.URLField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    api_url = forms.URLField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    miptaurl = forms.URLField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    
    def clean(self):
        uname = self.cleaned_data['username']
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['confirm_password']
        name = self.cleaned_data['operator_name']
        modes = self.cleaned_data['modes']
        homepage = self.cleaned_data['homepage']
        api_url = self.cleaned_data['api_url']
        miptaurl = self.cleaned_data['miptaurl']
        phone = self.cleaned_data['phone']
        email = self.cleaned_data['email'].strip()

        # check the user does not exist
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("This username is already taken.")
            
        # check the operator name does not exist
        if User.objects.filter(username=name).exists():
            raise forms.ValidationError("This operator name is already taken.")
        
        # check the passwords match
        if not password1 == password2:
            raise forms.ValidationError("The passwords do not match.")

        return self.cleaned_data
        
    def save(self, commit=True):
        m = super(RegisterForm, self).save(commit=False)
        m.username = self.cleaned_data['username']
        m.password = self.cleaned_data['password']
        if commit:
            m.save()
        return m

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'operator_name', 'modes', 'api_url', 'miptaurl', 'phone', 'email')

    