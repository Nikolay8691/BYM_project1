from django.http import HttpResponse
from functools import wraps

# Create your decorators here.
# def user_logged_in(f):
# 	@wraps(f)
# 	def wrapper(request, *args, **kwargs):
# 		if request.session['user_in']:
# 			return f(request, *args, **kwargs)
# 		else:
# 			return HttpResponse('you are not logged in as buyer, first create user_profile and then log in again')
# 	return wrapper

def user_logged_in(f):
	@wraps(f)
	def wrapper(request, *args, **kwargs):
		print('decorator user_logged_in is at work')
		try:
			if request.session['user_in']:
				return f(request, *args, **kwargs)
			else:
				return HttpResponse('you are not logged in as buyer, first create user_profile and then log in again')
		except KeyError:
				return HttpResponse('You are not even logged in!')
	return wrapper

def admin_logged_in(f):
	@wraps(f)
	def wrapper(request, *args, **kwargs):
		print('decorator admin_logged_in is at work')
		try:
			if request.session['admin_in']:
				return f(request, *args, **kwargs)
			else:
				return HttpResponse('you are not logged in as admin, yuo need to do the following: 1. submit request for admin_profile 2. log in again')
		except KeyError:
				return HttpResponse('You are not even logged in!')
	return wrapper
