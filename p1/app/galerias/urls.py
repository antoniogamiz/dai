from django.urls import path
from . import views

urlpatterns = [
    # galerias
    path('', views.vista_galerias, name='vista_galerias'),
    path('<int:id>', views.vista_galerias, name='vista_galerias_borrar'),
    path('crear_galeria', views.crear_nueva_galeria, name="crear_galeria"),
    path('actualizar_galeria/<int:id>', views.actualizar_galeria_vista, name="actualizar_galeria"),

    # cuadros
    path('cuadros/<int:galeria_id>', views.vista_cuadros, name='vista_cuadro'),
    path('cuadros/<int:galeria_id>/<int:id>', views.vista_cuadros, name='vista_cuadro_borrar'),
    path('cuadros/<int:galeria_id>/crear_cuadro', views.crear_nuevo_cuadro, name="crear_cuadro"),
    path('cuadros/<int:galeria_id>/actualizar_cuadro/<int:id>', views.actualizar_cuadro_vista, name="actualizar_cuadro"),
]
