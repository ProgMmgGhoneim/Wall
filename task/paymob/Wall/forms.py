from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Wall

class SignForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1' ,'password2' )


class WallForm(forms.ModelForm):
    class Meta:
        model = Wall
        fields = ('title', 'content', 'image')
