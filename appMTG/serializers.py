from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Carta, AlmacenCartas, Inventario, usuario_mtg


class CartasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carta
        fields = '__all__'


class AlmacenCartasSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlmacenCartas
        fields = '__all__'


class AlmacenCartasDetailSerializer(serializers.ModelSerializer):
    # Incluimos la carta completa para el inventario
    carta = CartasSerializer(read_only=True)

    class Meta:
        model = AlmacenCartas
        fields = ["id_almacen", "carta", "idioma", "es_foil", "cantidad"]


class InventarioDetailSerializer(serializers.ModelSerializer):
    almacen = AlmacenCartasDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Inventario
        fields = ["nombre_inventario", "usuario", "almacen"]


class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        # Exponemos el nombre del inventario (pk) y el usuario propietario
        fields = ["nombre_inventario", "usuario"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    # Don't show password in response
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validate_data):
        user = User.create_user(
            email=validate_data['email'],
            username=validate_data['username'],
            password=validate_data['password']
        )
        return user
