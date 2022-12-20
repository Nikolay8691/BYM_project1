from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:gp_product_id>/plus', views.plus, name = 'plus'),
    path('gcart_story', views.global_cart, name = 'gcart_story'),
    path('<int:gp_product2change_id>/change', views.change, name = 'change'),
    path('<int:gp_product2change_id>/delete', views.change_0, name = 'delete'),
    path('<int:user_id>/gc_userhistory', views.gc_userhistory, name = 'gc_userhistory'),
    path('<int:sales_id>/index_fromhistory', views.index_fromhistory, name = 'index_fromhistory'),
    # 
    path('<str:name>', views.hello, name = 'hello'),
]
