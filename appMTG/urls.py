from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import register, InventarioCartasViewSet, saveCardOne

router = DefaultRouter()
router.register(r'mis-inventarios', views.MisInventariosViewSet, basename='mis-inventarios')

inventario_cartas_list = InventarioCartasViewSet.as_view({"get": "list"})

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', register, name='register'),

    # Ejemplo: http://localhost:8000/api/usuarios/2/inventarios/Prueba/cartas/
    path(
        'usuarios/<int:id_user>/inventarios/<str:nombre_inventario>/cartas/',
        inventario_cartas_list,
        name='inventario-cartas-list'
    ),
    path('cartas/guardar-una/', saveCardOne, name='guardar-una-carta'),
]
