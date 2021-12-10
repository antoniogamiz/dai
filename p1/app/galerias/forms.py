from django.forms import ModelForm
from .models import Galeria, Cuadro


class GaleriaForm(ModelForm):
    class Meta:
        model = Galeria
        fields = ['nombre', 'direccion']


class CuadroForm(ModelForm):
    class Meta:
        model = Cuadro
        fields = ['nombre', 'galeria', 'autor', 'fecha_creacion']
