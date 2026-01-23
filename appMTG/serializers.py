from rest_framework import serializers
from .models import Carta, AlmacenCartas, Inventario


class CartasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carta
        fields = '__all__'


class AlmacenCartasSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlmacenCartas
        fields = '__all__'


class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        # Exponemos el nombre del inventario (pk) y el usuario propietario
        fields = ["nombre_inventario", "usuario"]
