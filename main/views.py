from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	if 'user_cart' not in request.session:
		request.session['user_cart'] = []

	user_cart = request.session['user_cart']
	# print(user_cart)
	return render(request, 'main/index.html', {
		'cart' : user_cart,
		})

def hello(request, name):
	return HttpResponse(f'glad to see you, {name.capitalize()}, and hello from the main_app!')
