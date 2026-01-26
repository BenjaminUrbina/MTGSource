from rest_framework import viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Inventario, Carta, AlmacenCartas
from .serializers import (
    InventarioSerializer,
    InventarioDetailSerializer,
    CartasSerializer,
    AlmacenCartasSerializer,
    UserRegistrationSerializer,
)


@permission_classes([AllowAny])
class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()

    def get_serializer_class(self):
        # Para list/retrieve devolvemos las cartas del inventario
        if self.action in ("list", "retrieve"):
            return InventarioDetailSerializer
        return InventarioSerializer


@permission_classes([AllowAny])
# Revisar manejo de caso de AttributeError
class CartasViewSet(viewsets.ModelViewSet):
    serializer_class = CartasSerializer
    queryset = Carta.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        id_scryfall = self.request.query_params.get("id_scryfall")

        if id_scryfall is None:  # sin parámetro: devuelve todas
            return qs

        id_scryfall = id_scryfall.strip()
        if not id_scryfall:
            raise ValidationError({"id_scryfall": "Parámetro inválido"})

        qs = qs.filter(id_scryfall=id_scryfall)
        if not qs.exists():
            raise NotFound("Carta no encontrada")

        return qs


@permission_classes([AllowAny])
class AlmacenCartasViewSet(viewsets.ModelViewSet):
    serializer_class = AlmacenCartasSerializer
    queryset = AlmacenCartas.objects.all()


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
