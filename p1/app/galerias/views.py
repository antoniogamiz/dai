from django.shortcuts import render
from django.http import HttpResponse
import logging
from django.urls import reverse

from .models import Galeria, Cuadro
from .forms import GaleriaForm, CuadroForm
logger = logging.getLogger(__name__)

# =================== GALERIAS =====================


def vista_galerias(request, id=None):
    """
      1. Si es un GET, devolvemos todas las galerias.
      2. Si es un DELETE, borramos la galeria que nos piden y volvemos a mostrarlas todas
    """
    if request.method == "DELETE":
        Galeria.objects.get(id=id).delete()

    context = {'galerias': Galeria.objects.all()}
    return render(request, 'galerias.html', context)


def actualizar_galeria_vista(request, id):
    """
    En esta vista hacemos dos cosas:
      1. Si es un POST, significa que estamos actualizando una galeria existente. Asi que
      inicializamos el formulario con los datos de la galeria y la actualizamos.
      Después, volvemos a mostrar el formulario de actualización con los nuevos datos.
      2. Si no es un POST, simplemente mostramos el formulario de actualización.
    """
    galeria = Galeria.objects.get(id=id)
    if request.method == 'POST':
        galeria = Galeria.objects.get(id=id)
        f = GaleriaForm(request.POST, instance=galeria)
        f.save()
    f = GaleriaForm(instance=galeria)
    f.form_action = reverse('actualizar_galeria', args=[id])
    context = {'form': f, 'actualizar': True}
    return render(request, 'crear_galeria.html', context)


def crear_nueva_galeria(request):
    """
    En esta vista hacemos dos cosas:
      1. Si es un POST, significa que estamos creando una nueva galeria. Asi que
      inicializamos el formulario con los datos de la request y guardamos la galeria.
      Después, volvemos a mostrar el formulario de creación.
      2. Si no es un POST, simplemente mostramos el formulario de creación.
    """
    if request.method == "POST":
        f = GaleriaForm(request.POST)
        f.save()
    context = {'form': GaleriaForm}
    return render(request, 'crear_galeria.html', context)

# =================== CUADROS =====================


def vista_cuadros(request, galeria_id=None, id=None):
    """
      1. Si es un GET, devolvemos todas los cuadros de la galería.
      2. Si es un DELETE, borramos el cuadro que nos piden y volvemos a mostrarlos todos.
    """
    if request.method == "DELETE":
        Cuadro.objects.get(id=id).delete()
    galeria = Galeria.objects.get(id=galeria_id)
    context = {'cuadros': Cuadro.objects.filter(galeria__id=galeria_id), 'galeria': galeria}
    return render(request, 'cuadros.html', context)


def actualizar_cuadro_vista(request, galeria_id, id):
    """
    En esta vista hacemos dos cosas:
      1. Si es un POST, significa que estamos actualizando una galeria existente. Asi que
      inicializamos el formulario con los datos de la galeria y la actualizamos.
      Después, volvemos a mostrar el formulario de actualización con los nuevos datos.
      2. Si no es un POST, simplemente mostramos el formulario de actualización.
    """
    cuadro = Cuadro.objects.get(id=id)
    if request.method == 'POST':
        f = CuadroForm(request.POST, instance=cuadro)
        f.save()
    f = CuadroForm(instance=cuadro)
    f.form_action = reverse('actualizar_cuadro', args=[galeria_id, id])
    galeria = Galeria.objects.get(id=galeria_id)
    context = {'form': f, 'actualizar': True, 'galeria': galeria}
    return render(request, 'crear_cuadro.html', context)


def crear_nuevo_cuadro(request, galeria_id):
    """
    En esta vista hacemos dos cosas:
      1. Si es un POST, significa que estamos creando un nuevo cuadro. Asi que
      inicializamos el formulario con los datos de la request y guardamos el nuevo cuadro.
      Después, volvemos a mostrar el formulario de creación.
      2. Si no es un POST, simplemente mostramos el formulario de creación.
    """
    if request.method == "POST":
        f = CuadroForm(request.POST)
        f.save()
    galeria = Galeria.objects.get(id=galeria_id)
    context = {'form': CuadroForm, 'galeria': galeria}
    return render(request, 'crear_cuadro.html', context)
