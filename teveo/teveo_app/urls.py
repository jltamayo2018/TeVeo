from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('camaras', views.cameras),
    path('comentario', views.comentario, name='comentario'),
    path('camaras/<str:id_camera>-dyn', views.camera_dyn, name='camera_dyn'),
    path('camaras/<str:id_camera>', views.camera_detail, name='camera_detail'),
]
