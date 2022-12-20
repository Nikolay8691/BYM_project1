from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('new_product', views.new_product, name = 'new_product'),
    path('<int:product_id>', views.product, name = 'product'),
    path('<int:price_list_id>/new_price', views.new_price, name = 'new_price'),
    path('<int:price_list_id>/add2price', views.add2price, name = 'add2price'),
    path('<int:price_list_id>/add2count', views.add2count, name = 'add2count'),
    # 
    path('<int:admin_id>/admin_prices', views.admin_prices, name = 'admin_prices'),
    path('<int:admin_id>/create_pricelist', views.create_pricelist, name = 'create_pricelist'),
    path('all_products', views.all_products, name = 'all_products'),
    path('<str:name>', views.hello, name = 'hello'),    
]
