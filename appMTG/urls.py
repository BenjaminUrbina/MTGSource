from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import current_user, register, InventarioCartasViewSet, saveCardOne

router = DefaultRouter()
router.register(r'mis-inventarios', views.MisInventariosViewSet, basename='mis-inventarios')

inventario_cartas_list = InventarioCartasViewSet.as_view({"get": "list"})

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', register, name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/me/', current_user, name='current-user'),

    # Ejemplo: http://localhost:8000/api/usuarios/2/inventarios/Prueba/cartas/
    path(
        'usuarios/<int:id_user>/inventarios/<str:nombre_inventario>/cartas/',
        inventario_cartas_list,
        name='inventario-cartas-list'
    ),
    path('cartas/guardar-una/', saveCardOne, name='guardar-una-carta'),
]
