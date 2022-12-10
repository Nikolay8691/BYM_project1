from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Product, PriceList, GlobalPrice, Category, Product_status
from .forms import AddForm

# Create your views here.
def index(request):
	request.session['index'] += ['products']

	price_lists = list(PriceList.objects.all())
	price_lists.sort(key = lambda price_list: price_list.date_x)
	price_list_today = price_lists[-1]
	
	gp_products = GlobalPrice.objects.filter(price_list = price_list_today)
	products = [gp.product for gp in gp_products]

	cart = list(request.session['user_cart'])
	gp_products_2 = []
	for gp in gp_products:
		qnt = 0
		for item in cart:
			if item[0] == gp.id:
				qnt = item[1]
		gp_products_2.append((gp, qnt))

	if request.method == 'GET' :
		prod_category = 'all'
		categories = Category.objects.all()

		return render(request, 'products/index.html', {
			# 'products' : products_prices,
			'gp_products' : gp_products_2,
			'prod_category' : prod_category,
			'categories' : categories,
			'price_list' : price_list_today,
			})

	elif request.method == 'POST' :
		prod_category = request.POST['category']

		products_all = Product.objects.all()
		products_in_category = [product for product in products_all if str(product.category) == prod_category] #5
		c = set(products_in_category) & set(products)
		gp_products_2c = [gp for gp in gp_products_2 if gp[0].product in c]

		return render(request, 'products/index_category.html', {
			# 'products' : products_prices,
			'gp_products' : gp_products_2c,
			'prod_category' : prod_category,
			'price_list' : price_list_today,
			})

	else:
		return HttpResponseRedirect(reverse('products:hello', args = ('nikolay',)))

def product(request, product_id):
	product = Product.objects.get(pk = product_id)
	return render(request, 'products/product.html', {
		'product' : product,
		})

def new_product(request):

	if request.method == 'POST':
		form = AddForm(request.POST)
		if form.is_valid():
			new_product = form.save()
			print(
				'products_title : ', new_product.title, 
				'admin : ', new_product.admin_madeby,
				'date on : ', new_product.date_created
				)
			return HttpResponseRedirect(reverse('products:product', args = (new_product.id,)))
		else:
			return render(request, 'products/new_product.html', {
				'form' : AddForm(form),
				'admin' : request.user,
				'categories' : Category.objects.all(),
				'status_all' : Product_status.objects.all(),
				})			
	else:
		return render(request, 'products/new_product.html', {
			'form' : AddForm(),
			'admin' : request.user,
			'categories' : Category.objects.all(),
			'status_all' : Product_status.objects.all(),
			})

def new_price(request, price_list_id):
	price_list = PriceList.objects.get(pk = price_list_id)
	price_list_items = GlobalPrice.objects.filter(price_list = price_list)

	gp_products = [gp_item.product for gp_item in price_list_items]
	extra_products = list(set(Product.objects.all()) - set(gp_products))
	return render(request, 'products/new_price.html', {
		'extra_products' : extra_products,
		'price_list_items' : price_list_items,
		'price_list' : price_list,
		})

def add2price(request, price_list_id):
	if request.method == 'POST' :
		price_list = PriceList.objects.get(pk=price_list_id)
		product = Product.objects.get(pk=int(request.POST['product']))
		return render(request, 'products/add2price.html', {
			'price_list' : price_list,
			'product' : product,
			})

def add2count(request, price_list_id):
	if request.method =='POST' :
		gp_product_productid = request.POST['product_id']
		gp_product_price = request.POST['product_price']

		gp_item = GlobalPrice(
			price_list = PriceList.objects.get(pk = price_list_id),
			product = Product.objects.get(pk = gp_product_productid),
			price = gp_product_price
			)
		gp_item.save()

		return HttpResponseRedirect(reverse('products:new_price', args = (price_list_id,)))

def hello(request, name):
	return HttpResponse(f' glad to see you, {name}, and hello from the products_app! ')

