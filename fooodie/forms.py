from django import forms
from fooodie.models import UserProfile, Photo
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm): 
    class Meta: 
        model = UserProfile 
        fields = ('picture',)
        
class UserSearchBarForm(forms.Form):
    username=forms.CharField()