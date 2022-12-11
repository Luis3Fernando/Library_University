from django.urls import path
from .views import *

app_name = "Repositorio"
urlpatterns = [
    path('', Login, name='Login'),
    path('home/<int:username_id>/<str:code>/', Home, name='home'),
    path('register/', Registrarse, name="Registrarse"),
    path('sala1/<str:id_user>', sala1, name="sala1"),
    path('checkview1', Chekview1, name="checkview1"),
    path('checkview2', Chekview2, name="checkview2"),
    path('sala2/', sala2, name='sala2'),
    path('checkview3', Checkview3, name='checkview3'),
    path('checkview4', Checkview4, name='checkview4'),
    path('send', send, name='send'),
    path('send2', send2, name='send2'),
    path('getMessages/<str:room>/', getMessages, name='getMessages'),
    path('home/<int:username_id>/<str:code>/subir/', subir, name='subir'),
    path('home/<int:username_id>/<str:code>/archivos/', Mostrar_Archivos, name='archivos'),
    path('home/<int:username_id>/<str:code>/mis_archivos/', Mis_Archivos, name='mis_archivos'),
    path('home/resultados/', Resultado_Busquedas, name='resultados'),
    path('home/archivos/<int:id_post>/<int:username_id>/', Archivo_personal, name='archivo_personal'),
    path('archivo', DescargarArchivoView.as_view(), name='archivo_post'),
]
