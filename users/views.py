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
from products.checkers import admin_logged_in, user_logged_in

# Create your views here.
def user_in(request):
	buyers = Profile_user.objects.all()
	buyers_user = [person.user for person in buyers]
	return request.user in buyers_user

def admin_in(request):
	admins = Profile_admin.objects.all()
	admins_user = [person.user for person in admins]
	return request.user in admins_user

@admin_logged_in
def index(request):
	admin = request.user
	return render(request, 'users/index.html', {
		'users' : User.objects.all(),
		'my_userid' : admin.id,
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
	        request.session['user_in'] = user_in(request)
	        request.session['admin_in'] = admin_in(request)
	        if 'index' not in request.session:
	        	request.session['index'] = ['users']
	        if 'user_cart' not in request.session:
	        	request.session['user_cart'] = []
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
			request.session['user_in'] = user_in(request)
			request.session['admin_in'] = admin_in(request)
			if 'index' not in request.session:
				request.session['index'] = ['users']
			if 'user_cart' not in request.session:
				request.session['user_cart'] = []

			return HttpResponseRedirect(reverse('users:user', args = (user.id,)))
		else:
			return render(request, 'users/login.html', {
				'msg_2' : {'msg_type' : 'negative', 'msg_text' : 'invalid username and/or password'},
				})
	return render(request, 'users/login.html')

def logout_view(request):
	logout(request)
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
		'msg_user' : request.session['user_in'],
		'msg_admin' : request.session['admin_in']
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
			# profile_birthday = form.cleaned_data['birthday']

			profile_birthday = request.POST['birthday']

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

			uprofile.save()
			request.session['user_in'] = user_in(request)
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

def user_look(request, user_id):
	person = User.objects.get(pk = user_id)
	user_profile = Profile_user.objects.get(user = person)
	return render(request, 'users/look_user.html', {
		'user' : user_profile,
		})

def admin_look(request, user_id):
	person = User.objects.get(pk = user_id)
	admin_profile = Profile_admin.objects.get(user = person)
	return render(request, 'users/look_admin.html', {
		'admin' : admin_profile,
		})