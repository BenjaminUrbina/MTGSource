from rest_framework import serializers
from models import PerfilUsuario


class PruebaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario  # De que modelo rescatamos los datos?
        fields = '__all__'  # Traeme todo
