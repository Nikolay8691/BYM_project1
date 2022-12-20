from django.shortcuts import render

from django.http import HttpResponse

from products.models import GlobalPrice

# Create your views here.
def index(request):
	request.session['index'] = ['main']
	if 'user_cart' not in request.session:
		request.session['user_cart'] = []

	# user_cart = request.session['user_cart']
	cart_id = request.session['user_cart']
	cart = [(GlobalPrice.objects.get(pk = gp_product_id), qnt) for gp_product_id, qnt in cart_id]
	return render(request, 'main/index.html', {
		'cart' : cart,
		'user' : request.user,
		'some_in' : ('user_in' or 'admin_in') in request.session,
		})

def hello(request):
	name = 'nikolay'
	return HttpResponse(f'glad to see you, {name.capitalize()}, and hello from the main_app!')
