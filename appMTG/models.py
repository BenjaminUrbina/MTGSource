from django.db import models
from django.contrib.auth.models import User


class usuario_mtg(models.Model):
    # AutoField para que sea autoincremental
    id_user = models.AutoField(primary_key=True)
    user = models.OneToOneField(  # Un usuario django = 1 perfil, mantiene unicidad
        User, on_delete=models.CASCADE,  # Eliminar cascada
        db_column="id_user_d")  # Nombre de la tabla
    nombre = models.TextField()

    class Meta:
        db_table = "usuario_mtg"

    def __str__(self):
        return f"{self.nombre} ({self.user.email})"


class Inventario(models.Model):
    nombre_inventario = models.CharField(primary_key=True, max_length=150)

    # FK a usuario_mtg
    usuario = models.ForeignKey(
        usuario_mtg,
        on_delete=models.CASCADE,   # si borras el usuario MTG, se borran los inventarios
        db_column="id_user"
    )

    class Meta:
        db_table = "inventario"

    def __str__(self):
        return f"{self.nombre_inventario} - {self.usuario.nombre}"


class Carta(models.Model):
    id_scryfall = models.CharField(primary_key=True, max_length=64)
    nombre = models.TextField()

    # URLField valida formato de URL, es mejor que TextField si realmente es una URL
    imagen_url = models.URLField(max_length=500)

    oracle_id = models.CharField(max_length=64)
    collector_number = models.IntegerField()
    set_code = models.CharField(max_length=20)
    type_line = models.TextField()

    class Meta:
        db_table = "cartas"

    def __str__(self):
        return self.nombre


class AlmacenCartas(models.Model):
    id_almacen = models.AutoField(primary_key=True)

    inventario = models.ForeignKey(
        Inventario,
        on_delete=models.CASCADE,      # si se borra el inventario, se borra su stock
        db_column="nombre_inventario",
        related_name="almacen"
    )

    carta = models.ForeignKey(
        Carta,
        # si borras una carta, se borran sus registros en inventarios
        on_delete=models.CASCADE,
        db_column="id_scryfall",
        related_name="en_inventarios"
    )

    idioma = models.CharField(max_length=10)
    es_foil = models.BooleanField(default=False)

    # cantidad no debería ser negativa
    cantidad = models.PositiveIntegerField()

    class Meta:
        db_table = "almacen_cartas"
        constraints = [
            models.UniqueConstraint(
                fields=["inventario", "carta", "idioma", "es_foil"],
                name="uniq_inventario_carta_idioma_foil"
            )
        ]

    def __str__(self):
        return f"{self.inventario_id} - {self.carta_id} ({self.idioma}, foil={self.es_foil}) x{self.cantidad}"
