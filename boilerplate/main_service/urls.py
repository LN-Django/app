from django.conf.urls import url
from django.urls import path

from .views.sample import SampleView
from .views.products import ProductsListView
from .views.product import ProductView

urlpatterns = [
    url('api/ping_main', SampleView.as_view()),
    url('api/products', ProductsListView.as_view(), name='get_post_products'),
    path('api/product/<int:product_id>',
         ProductView.as_view(), name='get_single_product')
]
