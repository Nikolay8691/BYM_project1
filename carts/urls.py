from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:gp_product_id>/plus', views.plus, name = 'plus'),
    path('gcart_story', views.global_cart, name = 'gcart_story'),
    path('<int:gp_product2change_id>/change', views.change, name = 'change'),
    # 
    path('<str:name>', views.hello, name = 'hello'),
]
