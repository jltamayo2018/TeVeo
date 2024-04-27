from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    # str indica que tiene que ser exactamente un string
    path('camaras', views.cameras),
    path('comentario', views.comentario),
    # path('<str:comentario_camaras>', views.decide_option),
]