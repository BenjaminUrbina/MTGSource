from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import register

router = DefaultRouter()
router.register(r'inventario', views.InventarioViewSet, basename='inventario')
router.register(r'cartas', views.CartasViewSet, basename='cartas')
router.register(r'almacen', views.AlmacenCartasViewSet, basename='almacen')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', register, name='register'),
]
