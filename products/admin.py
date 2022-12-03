from django.contrib import admin
from .models import Product, PriceList, SaleList, GlobalPrice, Category, Product_status

# Register your models here.
admin.site.register(PriceList)
admin.site.register(SaleList)
admin.site.register(Product)
admin.site.register(GlobalPrice)
admin.site.register(Category)
admin.site.register(Product_status)
