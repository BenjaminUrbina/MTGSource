from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Inventario, Carta, AlmacenCartas, usuario_mtg
from .serializers import (
    AlmacenCartaSerializer,
    CartaSerializer,
    CurrentUserSerializer,
    InventarioResumenSerializer,
    UserRegistrationSerializer,
    SaveCardOneSerializer,
)
from django.db import transaction
from django.db.models import F


class MisInventariosViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Devuelve los inventarios del usuario autenticado (solo nombre y ultima_vez).
    GET /mis-inventarios/
    """
    serializer_class = InventarioResumenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
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
        is_owner = False
        if self.request.user and self.request.user.is_authenticated:
            is_owner = (inventario.usuario.user_id == self.request.user.id)

        if is_owner:
            pass
        else:
            if inventario.is_public:
                pass
            else:
                if not inventario.is_sharing_enabled:
                    raise PermissionDenied(
                        "Este inventario no es público ni está compartido.")
                if not token or token != inventario.share_token:
                    raise PermissionDenied("Token inválido o faltante.")

        return (
            AlmacenCartas.objects
            .filter(inventario=inventario)
            .select_related("carta")
            .order_by("carta__nombre")
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def saveCardOne(request):
    """
    Función que recibe un json, el cual obtiene una carta y tiene que agregarla a la base de datos

    Usa: 
    - El token del usuario para poder validar y asegurarse que es el user.
    - Nombre del inventario a cual quiera agregarle la carta.
    - La carta que quiere agregar.

    Retorna:
    - 201 cuando se cree todo con exito.
    - 401 en caso que no este autenticado.
    - 403 en caso que intente insertar la carta pero no sea su inventario.
    - 404 en caso de que no encuentre el inventario.    
    """

    serializer = SaveCardOneSerializer(data=request.data)

    if serializer.is_valid():
        # Aqui tendria que ir la validacion para el user

        data = serializer.validated_data

        try:
            usuarioMTG = usuario_mtg.objects.filter(
                id_user=data["id_mtg_user"],
                nombre=data['nombre_user_mtg']
            ).first()
            if not usuarioMTG:
                raise NotFound("Usuario MTG no existe.")

            inventario_view = Inventario.objects.filter(
                usuario=usuarioMTG,
                nombre_inventario=data['nombre_inventario'],
            ).first()
            if not inventario_view:
                raise NotFound("Inventario no existe.")

            carta_view, _ = Carta.objects.get_or_create(
                id_scryfall=data['id_scryfall_carta'],
                defaults={
                    "scryfall_uri": data.get('scryfall_uri_carta'),
                    "prints_search_uri": data.get('prints_search_uri'),
                    "nombre": data['nombre_carta'],
                    "purchase_uris": data.get('purchase_uris_carta'),
                    "border_color": data.get('border_color', "black"),
                    "full_art": data.get('full_art', False),
                    "promo": data.get('promo', False),
                    "imagen_url": data['imagen_url'],
                    "oracle_id": data['oracle_id'],
                    "collector_number": data['collector_number'],
                    "set_code": data['set_code'],
                    "type_line": data['type_line'],
                },
            )

            with transaction.atomic():
                almacen, created = AlmacenCartas.objects.get_or_create(
                    inventario=inventario_view,
                    carta=carta_view,
                    idioma=data['idioma_carta'],
                    es_foil=data.get('es_foil_carta', False),
                    defaults={"cantidad": 1},
                )
                if not created:
                    AlmacenCartas.objects.filter(pk=almacen.pk).update(
                        cantidad=F("cantidad") + 1
                    )
                    almacen.refresh_from_db()

            return Response(
                {"id_almacen": almacen.id_almacen, "cantidad": almacen.cantidad},
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )
        except NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user and return JWT token"""
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'token': str(refresh.access_token),
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': CurrentUserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response(CurrentUserSerializer(request.user).data, status=status.HTTP_200_OK)
