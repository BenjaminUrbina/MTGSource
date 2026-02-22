from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Carta, AlmacenCartas, Inventario, usuario_mtg


class CartaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carta
        fields = [
            "id_scryfall",
            "nombre",
            "imagen_url",
            "oracle_id",
            "collector_number",
            "set_code",
            "type_line",
            "border_color",
            "full_art",
            "promo",
            "scryfall_uri",
            "prints_search_uri",
            "purchase_uris",
        ]


class AlmacenCartaSerializer(serializers.ModelSerializer):
    # Esto “anida” la carta completa dentro del objeto del stock
    carta = CartaSerializer(read_only=True)

    class Meta:
        model = AlmacenCartas
        fields = [
            "id_almacen",
            "idioma",
            "es_foil",
            "cantidad",
            "carta",
        ]


class InventarioResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = ["nombre_inventario", "ultima_vez"]


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


class SaveCardOneSerializer(serializers.Serializer):
    id_mtg_user = serializers.IntegerField()
    nombre_user_mtg = serializers.CharField()
    nombre_inventario = serializers.CharField()

    id_scryfall_carta = serializers.CharField()
    scryfall_uri_carta = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    prints_search_uri = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    nombre_carta = serializers.CharField()
    purchase_uris_carta = serializers.JSONField(required=False, allow_null=True)
    border_color = serializers.CharField(required=False, default="black")
    full_art = serializers.BooleanField(required=False, default=False)
    promo = serializers.BooleanField(required=False, default=False)
    imagen_url = serializers.URLField()
    oracle_id = serializers.CharField()
    collector_number = serializers.IntegerField()
    set_code = serializers.CharField()
    type_line = serializers.CharField()

    idioma_carta = serializers.CharField()
    es_foil_carta = serializers.BooleanField(required=False, default=False)
