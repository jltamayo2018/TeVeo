from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('camaras/', views.cameras),
    path('comentario/', views.comentario),
    path('camaras/<str:id_camera>/', views.camera_detail, name='camera_detail'),
]
# path('<str:comentario_camaras>', views.decide_option),
