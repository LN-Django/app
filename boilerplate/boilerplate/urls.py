from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from os import environ

# ! Cannot be found. @see https://stackoverflow.com/questions/47563013/unable-to-import-path-from-django-urls
# from django.urls import path

app_name = environ.get('DJANGO_APP_NAME', default="local")

protocol = 'http' if environ.get('DEBUG', default=1) == 1 else 'https'
docs_base_url = app_name + '.herokuapp.com' if app_name != "local" else 'localhost:8000'
docs_url = protocol + "://" + docs_base_url + "/api/v1"

schema_view = get_schema_view(
    openapi.Info(
        title="App Service API",
        default_version='v0.0.1',
        description="Application Service",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="louisandrew3@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    url=docs_url
)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('main_service.urls')),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^api/v1/swagger/$', schema_view.with_ui('swagger',
        cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api/v1/redoc/$', schema_view.with_ui('redoc',
        cache_timeout=0), name='schema-redoc'),
]
