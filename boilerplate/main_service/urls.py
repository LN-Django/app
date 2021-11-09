from django.conf.urls import url
from .views import MainServiceView

urlpatterns = [
    url('api/ping_main', MainServiceView.as_view())
]
