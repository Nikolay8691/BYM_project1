from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from products.models import GlobalPrice, SaleList
from users.models import Profile_user
from .models import GlobalCart
from products.checkers import admin_logged_in, user_logged_in
from datetime import date, datetime

# Create your views here.

@user_logged_in
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
		if pcs > 0:
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

@user_logged_in
def gc_userhistory(request, user_id):
	user_profile = Profile_user.objects.get(pk = user_id)
	s_lists = user_profile.buyer.all()

	gc_usersum, gc_usersales = (0, [])
	for s_list in s_lists:
		gc_products = s_list.slist_by.all()
		gc_qnt, gc_sum, gc_usercart = (0, 0, [])
		for gc_product in gc_products:
			gc_usercart.append(gc_product)
			gc_qnt += gc_product.qnt
			gc_sum += gc_product.qnt * gc_product.gp_product.price
		gc_usersum += gc_sum
		gc_sale = [gc_usercart, gc_qnt, gc_sum, len(gc_usercart), (s_list.id, s_list.date_y)]
		gc_usersales.append(gc_sale)

	return render(request, 'carts/gc_userhistory.html', {
		'user_carts' : gc_usersales,
		'user_sum' : gc_usersum,
		'user_sales' : len(gc_usersales),
		'user' : user_profile,
		})

def index_fromhistory(request, sales_id):
	user_profile = Profile_user.objects.get(user = request.user)
	s_list = SaleList.objects.get(pk = sales_id)
	gc_products = s_list.slist_by.all()

	gc_qnt, gc_sum, gc_usercart = (0, 0, [])
	for gc_product in gc_products:
		gc_usercart.append(gc_product)
		gc_qnt += gc_product.qnt
		gc_sum += gc_product.qnt * gc_product.gp_product.price

	return render(request, 'carts/index_fromhistory.html', {
		'user_cart' : gc_usercart,
		'cart_sum' : gc_sum,
		'cart_qnt' : gc_qnt,
		'user' : user_profile,
		'slist_data' : (s_list.id, s_list.date_y),
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
			'from_app' : list(request.session['index'])[-1],
			})
	elif request.method == 'POST':
		old = [gp_product2change_id, gp_product2change_qnt]
		request.session['user_cart'].remove(old)
		request.session.modified = True
		new_qnt = int(request.POST['pcs'])
		if new_qnt > 0:
			new_item = (gp_product2change_id, new_qnt)
			request.session['user_cart'] += [new_item]

		from_app = list(request.session['index'])[-1]
		if from_app == 'products':
			return HttpResponseRedirect(reverse('products:index'))
		else:
			return HttpResponseRedirect(reverse('carts:index'))
	else:
		return HttpResponseRedirect(reverse('carts:hello', args = ('nikolay',)))

def change_0(request, gp_product2change_id):
	cart_id = (request.session['user_cart'])
	gp_product2change = GlobalPrice.objects.get(pk = gp_product2change_id)

	for cart_item in cart_id:
		gp_product_id, qnt = cart_item
		if gp_product_id == gp_product2change_id:
			gp_product2change_qnt = qnt

	old = [gp_product2change_id, gp_product2change_qnt]
	request.session['user_cart'].remove(old)
	request.session.modified = True

	return HttpResponseRedirect(reverse('carts:index'))

def hello(request, name):
	return HttpResponse(f' glad to see you, {name}, and hello from the carts_app! ')
