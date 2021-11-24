from django.conf.urls import url
from django.urls import path


from .views.products_to_csv import ProductToCSVView
from .views.product import ProductView
from .views.products import ProductsListView
from .views.sample import SampleView
from .views.product_info import ProductInfoView
from .views.all_products_info import AllProductsInfoView

urlpatterns = [
    url('api/ping_main', SampleView.as_view()),
    # note: Define before the `api/products endpoint`
    path('api/products/info', AllProductsInfoView.as_view(),
         name='get_all_products_info'),
    path('api/products/csv', ProductToCSVView.as_view(),
         name='get_products_as_csv'),
    url('api/products', ProductsListView.as_view(), name='get_post_products'),
    path('api/product/<int:product_id>',
         ProductView.as_view(), name='get_single_product'),
    path('api/product/<int:product_id>/info',
         ProductInfoView.as_view(), name='get_single_product_info'),
]
