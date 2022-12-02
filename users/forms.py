from django import forms

# Create your forms here.

class ProfileForm(forms.Form):
	f_name = forms.CharField(label = 'first name ', min_length = 1, max_length = 64)
	l_name = forms.CharField(label = 'last name ', min_length = 1, max_length = 64)
	email = forms.EmailField(label = 'e-mail ', empty_value = 'user@ya.ru')
	phone = forms.CharField(label = 'phone ', min_length = 1, max_length = 64)
	age = forms.IntegerField(label = 'age ', max_value = 65, required = False)
	sex = forms.CharField(label = 'sex ', required = False)
	birthday = forms.DateField(label = 'birthday date (YYYY-MM-DD) ', required = False)

class AdminData(forms.Form):
	nick = forms.CharField(label = 'nickname ', min_length = 1, max_length = 16)
	f_name = forms.CharField(label = 'first name ', min_length = 1, max_length = 64)
	l_name = forms.CharField(label = 'last name ', min_length = 1, max_length = 64)
	email = forms.EmailField(label = 'e-mail ', empty_value = 'admin@ya.ru')
	phone = forms.CharField(label = 'phone ', required = False)
