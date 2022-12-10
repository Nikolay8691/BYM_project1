from django.db import models

from products.models import GlobalPrice, SaleList

# Create your models here.
class GlobalCart(models.Model):
	sales_list = models.ForeignKey(SaleList, on_delete = models.CASCADE, related_name = 'slist_by')
	gp_product = models.ForeignKey(GlobalPrice, on_delete = models.CASCADE, related_name = 'gp_by')
	qnt = models.IntegerField()

	def __str__(self):
		return f'{self.sales_list} : {self.gp_product.product.title} at {self.gp_product.price} * {self.qnt}'
