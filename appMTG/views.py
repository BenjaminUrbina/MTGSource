from django.http import JsonResponse
from .models import Inventario


def sacar_todo(request):
    mi_inventario = Inventario.objects.all()

    inventarios_list = [
        {
            'nombre': inv.nombre_inventario,
            'usuario': inv.usuario.nombre
        }
        for inv in mi_inventario
    ]

    return JsonResponse({'inventarios': inventarios_list})
