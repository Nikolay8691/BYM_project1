from django import forms
from django.forms import ModelForm

from .models import Profile_user, Profile_admin

# Create your forms here.

class ProfileForm(ModelForm):
	class Meta:
		model = Profile_user
		exclude = ['user', 'birthday']

class AdminData(ModelForm):
	class Meta:
		model = Profile_admin
		exclude = ['user']
