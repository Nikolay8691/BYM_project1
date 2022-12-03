from django.db import models
from datetime import date, datetime

# from django.contrib.auth.models import User

from users.models import Profile_user, Profile_admin

# Create your models here.

class PriceList(models.Model):
	creator = models.ForeignKey(Profile_admin, on_delete = models.CASCADE, related_name = 'created_by')
	date_x = models.DateField(default = date.today, blank = True)

	def __str__(self):
		return f' Price list on {self.date_x} created by {self.creator}'

class SaleList(models.Model):
	buyer = models.ForeignKey(Profile_user, on_delete = models.CASCADE, related_name = 'buyer')
	date_y = models.DateField(default = datetime.now, blank = True)

	def __str__(self):
		return f' Sale list of {self.buyer} dated {self.date_y}'

class Category(models.Model):
	title = models.CharField(max_length = 32)

	def __str__(self):
		return f' category : {self.title}'

	class Meta:
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'

class Product_status(models.Model):
	state = models.CharField(max_length = 32)

	def __str__(self):
		return f' status : {self.state}'

	class Meta:
		verbose_name = 'Produst status'
		verbose_name_plural = 'Product status all'	

class Product(models.Model):
	title = models.CharField(max_length = 64)
	category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'category_in')
	state = models.ForeignKey(Product_status, on_delete = models.CASCADE, related_name = 'state_in')
	description = models.TextField(blank = True)
	photo = models.ImageField(upload_to = 'images', blank = True)
	sale_lists = models.ManyToManyField(SaleList, blank = True, related_name = 'sold_in')
	admin_madeby = models.ForeignKey(Profile_admin, on_delete = models.CASCADE, related_name = 'admin_by')
	date_created = models.DateField(default = datetime.now, blank = True)


	def __str__(self):
		return f' Product : {self.title}, Category : {self.category}, State : {self.state}'

class GlobalPrice(models.Model):
	price_list = models.ForeignKey(PriceList, on_delete = models.CASCADE, related_name = 'by_price_list')
	product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'by_product')
	price = models.FloatField(default = 1)

	def __str__(self):
		return f' Product : {self.product.title} {self.price} priced_date {self.price_list.date_x}'
