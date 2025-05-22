"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions

# swagger
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# class JWTSchemaGenerator(OpenAPISchemaGenerator):
#     def get_security_definitions(self):
#         security_definitions = super().get_security_definitions()
#         security_definitions['Bearer'] = {
#             'type': 'apiKey',
#             'name': 'Authorization',
#             'in': 'header',
#         }
#         return security_definitions


schema_view = get_schema_view(
    openapi.Info(
        title='Effective Mobile task',
        default_version='v1',
        description='Effective Mobile Python task api documentation',
        terms_of_service='',
        contact=openapi.Contact(email='smth@gmail.com'),
        license=openapi.License(name="Some license"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    # generator_class=JWTSchemaGenerator,

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # adds basic login/logout views
    path('accounts/', include('django.contrib.auth.urls')),

    path('api/', include('ads.urls')),
    # swagger codes
    #auth not working
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
