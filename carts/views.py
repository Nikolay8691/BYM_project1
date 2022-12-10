from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from products.models import GlobalPrice, SaleList
from users.models import Profile_user
from .models import GlobalCart

from datetime import date, datetime

# Create your views here.

def index(request):
	request.session['index'] += ['carts']
	cart_id = (request.session['user_cart'])
	cart = [(GlobalPrice.objects.get(pk = gp_product_id), qnt) for gp_product_id, qnt in cart_id]
	return render(request, 'carts/index.html', {
		'cart' : cart,
	})

def plus(request, gp_product_id):
	gp_product = GlobalPrice.objects.get(pk = gp_product_id)
	if request.method == 'POST':
		pcs = int(request.POST['pcs'])
		item = (gp_product_id, pcs) # item = (gp_product, pcs) - can't keep gp_product tuple in sessions
		request.session['user_cart'] += [item]

	return HttpResponseRedirect(reverse('products:index'))

def global_cart(request):
	user = request.user
	profile_user = Profile_user.objects.get(user = user)
	s_list = SaleList(buyer = profile_user, date_y = datetime.now())
	s_list.save()

	cart_products = []
	cart_sum = 0
	cart_qnt = 0
	cart_id = (request.session['user_cart'])
	for cart_item in cart_id:
		gp_product_id, qnt = cart_item
		gp_product = GlobalPrice.objects.get(pk = gp_product_id)
		sales_item = GlobalCart(sales_list = s_list, gp_product = gp_product, qnt = qnt)
		sales_item.save()
		cart_products.append(gp_product.product)
		cart_sum += qnt * gp_product.price
		cart_qnt += qnt

	return render(request, 'carts/gcart_story.html', {
		'products' : cart_products,
		'story' : s_list,
		'sum' : cart_sum,
		'qnt' : cart_qnt,
		})

def change(request, gp_product2change_id):
	cart_id = (request.session['user_cart'])
	gp_product2change = GlobalPrice.objects.get(pk = gp_product2change_id)

	for cart_item in cart_id:
		gp_product_id, qnt = cart_item
		if gp_product_id == gp_product2change_id:
			gp_product2change_qnt = qnt

	if request.method == 'GET':
		return render(request, 'carts/gp2change_incart.html', {
			'gp_product' : (gp_product2change.product.title, gp_product2change_qnt),
			})
	elif request.method == 'POST':
		old = [gp_product2change_id, gp_product2change_qnt]
		request.session['user_cart'].remove(old)
		new_qnt = int(request.POST['pcs'])
		new_item = (gp_product2change_id, new_qnt)
		request.session['user_cart'] += [new_item]

		from_app = list(request.session['index'])[-1]
		if from_app == 'products':
			return HttpResponseRedirect(reverse('products:index'))
		else:
			return HttpResponseRedirect(reverse('carts:index'))
	else:
		return HttpResponseRedirect(reverse('carts:hello', args = ('nikolay',)))

def hello(request, name):
	return HttpResponse(f' glad to see you, {name}, and hello from the carts_app! ')
