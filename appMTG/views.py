from .serializers import AlmacenCartaSerializer
from .models import AlmacenCartas, Inventario
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Inventario, Carta, AlmacenCartas, usuario_mtg
from .serializers import (
    CartaSerializer,
    InventarioResumenSerializer,
    AlmacenCartaSerializer,
    UserRegistrationSerializer,
)


class MisInventariosViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Devuelve los inventarios del usuario autenticado (solo nombre y ultima_vez).
    GET /mis-inventarios/
    """
    serializer_class = InventarioResumenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # request.user es el User de Django
        perfil = usuario_mtg.objects.get(user=self.request.user)

        return (
            Inventario.objects
            .filter(usuario=perfil)
        )


@permission_classes([AllowAny])
# Revisar manejo de caso de AttributeError
class CartasViewSet(viewsets.ModelViewSet):
    serializer_class = CartaSerializer
    # Cambiar a [IsAuthenticated] si corresponde
    permission_classes = [AllowAny]
    # url = /cartas/<valor>/ | lookup_field = "valor"
    lookup_field = "id_scryfall"

    def get_queryset(self):
        return Carta.objects.only("id_scryfall", "nombre")


class InventarioCartasViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AlmacenCartaSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        id_user = self.kwargs.get("id_user")
        nombre_inventario = self.kwargs.get("nombre_inventario")
        # token desde ?token=...
        token = self.request.query_params.get("token")

        inventario = (
            Inventario.objects
            .select_related("usuario", "usuario__user")
            .filter(nombre_inventario=nombre_inventario, usuario_id=id_user)
            .first()
        )
        if not inventario:
            raise NotFound("Inventario no existe.")

        # 1) Si el request viene con usuario autenticado, verificar si es dueño
        is_owner = False
        if self.request.user and self.request.user.is_authenticated:
            is_owner = (inventario.usuario.user_id == self.request.user.id)

        # 2) Si es dueño: acceso total
        if is_owner:
            pass
        else:
            # 3) Si NO es dueño: permitir SOLO si el inventario es público/compartible
            #    Reglas recomendadas:
            #    - Si is_public=True => cualquiera puede ver sin token
            #    - Si is_public=False => solo si is_sharing_enabled=True y token coincide

            if inventario.is_public:
                pass
            else:
                if not inventario.is_sharing_enabled:
                    raise PermissionDenied(
                        "Este inventario no es público ni está compartido.")
                if not token or token != inventario.share_token:
                    raise PermissionDenied("Token inválido o faltante.")

        # 4) Retornar cartas del inventario
        return (
            AlmacenCartas.objects
            .filter(inventario=inventario)
            .select_related("carta")
            .order_by("carta__nombre")
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user and return JWT token"""
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        # Generate JWT token
        refresh = RefreshToken.for_user(user)

        return Response({
            'token': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
