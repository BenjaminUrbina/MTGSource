from django.urls import path
from . import views

urlpatterns = [
    path('', views.sacar_todo, name='lista_inventarios')
]
