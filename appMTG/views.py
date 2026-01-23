from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from .models import Inventario, Carta, AlmacenCartas
from .serializers import InventarioSerializer, CartasSerializer, AlmacenCartasSerializer


class InventarioViewSet(viewsets.ModelViewSet):
    serializer_class = InventarioSerializer
    queryset = Inventario.objects.all()


class CartasViewSet(viewsets.ModelViewSet):
    serializer_class = CartasSerializer
    queryset = Carta.objects.values_list()  # base

    def get_queryset(self):
        qs = super().get_queryset()
        id_scryfall = self.request.query_params.get("id_scryfall")
        if id_scryfall:
            qs = qs.filter(id_scryfall=id_scryfall)
            if not qs.exists():
                raise NotFound("Carta no encontrada")
        return qs


class AlmacenCartasViewSet(viewsets.ModelViewSet):
    serializer_class = AlmacenCartasSerializer
    queryset = AlmacenCartas.objects.all()
