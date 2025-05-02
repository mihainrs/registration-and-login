from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models
        
class RegisterAccount(UserCreationForm):
    
    # init method so that we may begin editing the fields, adding
    # placeholders and such
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder' : 'Enter your username'
        })
        
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder' : 'Enter your first name'
        })
        
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder' : 'Enter your last name'
        })
        
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder' : 'example@domain.com'
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder' : 'Enter your password'
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder' : 'Confirm your password'
        })
    
    username = forms.CharField(max_length= 150)
    first_name = forms.CharField(max_length= 150)
    last_name = forms.CharField(max_length= 150)
    email = forms.EmailField(max_length= 150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']#

#the login form

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'class':'form-control',
            'placeholder':'Username goes here'
        })
        
        self.fields['password'].widget.attrs.update({
            'class':'form-control'
        })