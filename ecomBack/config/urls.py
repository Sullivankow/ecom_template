"""
Configuration des URLs pour le projet config.

La liste `urlpatterns` relie les URLs aux vues. Pour plus d'informations, voir :
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Exemples :
Vues fonctionnelles
    1. Ajouter un import :  from my_app import views
    2. Ajouter une URL à urlpatterns :  path('', views.home, name='home')
Vues basées sur les classes
    1. Ajouter un import :  from other_app.views import Home
    2. Ajouter une URL à urlpatterns :  path('', Home.as_view(), name='home')
Inclure une autre configuration d'URL
    1. Importer la fonction include : from django.urls import include, path
    2. Ajouter une URL à urlpatterns :  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin

schema_view = get_schema_view(
    openapi.Info(
        title="API e-commerce",
        default_version='v1',
        description="Documentation de l'API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
     path('admin/', admin.site.urls),
     re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/users/', include('users.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        
]