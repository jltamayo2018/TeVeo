from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('camaras', views.cameras, name='camaras'),
    path('comentario', views.comentario, name='comentario'),
    path('camaras/<str:id_camera>-dyn', views.camera_dyn, name='camera_dyn'),
    path('camaras/<str:id_camera>', views.camera_detail, name='camera_detail'),
    path('ayuda', views.help, name='help'),
    path('config', views.settings, name='settings'),
    path('camaras/<str:id_camera>/camaras-json', views.camera_json, name='camera_json'),
    path('cambio/<str:cookie>', views.cambio, name='cambio'),
]
