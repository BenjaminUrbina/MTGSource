from django.contrib import admin
from .models import usuario_mtg, Inventario, Carta, AlmacenCartas


@admin.register(usuario_mtg)
class UsuarioMtgAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'nombre', 'user')
    search_fields = ('nombre', 'user__email')


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_inventario', 'usuario')
    list_filter = ('usuario',)
    search_fields = ('nombre_inventario',)


@admin.register(Carta)
class CartaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'set_code', 'collector_number', 'type_line')
    search_fields = ('nombre', 'set_code', 'oracle_id')
    list_filter = ('set_code',)


@admin.register(AlmacenCartas)
class AlmacenCartasAdmin(admin.ModelAdmin):
    list_display = ('carta', 'inventario', 'cantidad', 'idioma', 'es_foil')
    list_filter = ('idioma', 'es_foil', 'inventario')
    search_fields = ('carta__nombre', 'inventario__nombre_inventario')
