from django.conf.urls import url
from .views.sample import SampleView
from .views.products import ProductsListView

urlpatterns = [
    url('api/ping_main', SampleView.as_view()),
    url('api/products', ProductsListView.as_view())
]
