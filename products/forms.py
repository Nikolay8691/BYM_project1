from django import forms
from django.forms import ModelForm

from .models import Product
# Create your forms here.

class AddForm(ModelForm):
	class Meta:
		model = Product
		fields = '__all__'

