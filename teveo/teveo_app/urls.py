from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('camaras', views.cameras),
    path('comentario', views.comentario),
    # path('<str:comentario_camaras>', views.decide_option),
]