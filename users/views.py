from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from .forms import ProfileForm, AdminData
from .models import Profile_user, Profile_admin

from urllib.parse import urlencode

from datetime import date

# Create your views here.
def index(request):
	return render(request, 'users/index.html', {
		'users' : User.objects.all()
		})

def register(request):
	if request.method == "GET":
	    return render(
	        request, 'users/register.html', {
	        'form': UserCreationForm,
	        'msg_1' : {'msg_type' : 'neutral', 'msg_text' : 'welcome to start registration!'},
	    	})
	elif request.method == "POST":
	    form = UserCreationForm(request.POST)
	    if form.is_valid():
	        user = form.save()            
	        login(request, user)
	        return HttpResponseRedirect(reverse('users:user_profile', args = (user.id,)))
	    else:
	        return render(
	            request, 'users/register.html', {
	            'form': UserCreationForm,
	            'msg_1' : {'msg_type' : 'negative', 'msg_text' : 'invalid registration form data'},            
	        	})

def login_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('users:user', args = (user.id,)))
		else:
			return render(request, 'users/login.html', {
				'msg_2' : {'msg_type' : 'negative', 'msg_text' : 'invalid username and/or password'},
				})

	return render(request, 'users/login.html')

def logout_view(request):
	logout(request)
	request.session['user_cart'] = []
	return render(request, 'users/login.html', {
		'msg_2' : {'msg_type' : 'negative', 'msg_text' : 'Logged out'},
		})

def user(request, user_id):
	user = User.objects.get(pk = user_id)
	message = request.GET.get('message')
	if message == None:
		msg_2 = {'msg_type' : 'positive', 'msg_text' : 'from user login'}
	else:
		msg_2 = {'msg_type' : 'neutral', 'msg_text' : message}

	return render(request, 'users/user.html', {
		'user' : user,
		'msg_2' : msg_2,
		})

def uprofile(request, user_id):

	user = User.objects.get(pk = user_id)
	profile_user = user
	if request.method == 'POST':

		form = ProfileForm(request.POST)
		if form.is_valid():
			profile_first = form.cleaned_data['f_name']
			profile_last = form.cleaned_data['l_name']
			profile_email = form.cleaned_data['email']
			profile_phone = form.cleaned_data['phone']
			profile_age = form.cleaned_data['age']
			profile_sex = form.cleaned_data['sex']
			profile_birthday = form.cleaned_data['birthday']

			# if profile_age == None:
			# 	profile_age = 0
			# if profile_birthday == None:
			# 	profile_birthday = date.today()

			uprofile = Profile_user(
				user = profile_user,
				f_name = profile_first,
				l_name = profile_last,
				email = profile_email,
				phone = profile_phone,
				age = profile_age,
				sex = profile_sex,
				birthday = profile_birthday
				)

			# print(
			# 	uprofile.user.username, type(uprofile.user.username),
			# 	uprofile.f_name, type(uprofile.f_name),
			# 	uprofile.l_name, type(uprofile.l_name),
			# 	uprofile.email, type(uprofile.email),
			# 	uprofile.phone, type(uprofile.phone),
			# 	uprofile.age, type(uprofile.age),
			# 	uprofile.sex, type(uprofile.sex),
			# 	uprofile.birthday, type(uprofile.birthday)
			# 	)


			uprofile.save()

			return HttpResponseRedirect(reverse('users:user', args = (user.id,)))
		else:
			return render(request, 'users/uprofile.html', {
				'form' : form,
				'user' : user,
				'msg_3' : {'msg_type' : 'negative', 'msg_text' : 'sos!.. from user profile'},
				})
	else:

		return render(request, 'users/uprofile.html', {
			'form' : ProfileForm(),
			'user' : user,
			'msg_3' : {'msg_type' : 'neutral', 'msg_text' : 'from user register'},
			})

def admin_data(request, user_id):

	user = User.objects.get(pk = user_id)
	data_user = user
	if request.method == 'POST':
		
		form = AdminData(request.POST)
		if form.is_valid():
			admin_data = form.save(commit = False)
			admin_data.user = data_user
			
			# print(
			# 	admin_data.user.username,
			# 	admin_data.nick,
			# 	admin_data.f_name,
			# 	admin_data.l_name,
			# 	admin_data.email,
			# 	admin_data.phone,
			# 	)

			admin_data.save()

			user_url = reverse('users:user', args = (user.id,))
			# return HttpResponseRedirect(user_url)
			
			msg_4 = 'the admin_request is on. confirmation takes 24-120 hours. wait for email. thanks!'
			msg_text = urlencode({'message' : msg_4})
			url = f'{user_url}?{msg_text}'
			return redirect(url)

		else: 
			return render(request, 'users/admin_data.html', {
				'form' : form,
				'user' : user,
				'msg_3' : {'msg_type' : 'negative', 'msg_text' : 'sos!.. from admin register'},
				})

	else:

		return render(request, 'users/admin_data.html', {
			'form' : AdminData(),
			'user' : user,
			'msg_3' : {'msg_type' : 'neutral', 'msg_text' : 'from admin register'},
			})
