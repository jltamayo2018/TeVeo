from django.shortcuts import render
from django.http import HttpResponse
from .models import Camera, Comment
from . import utils
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings

BASE_DIR = settings.BASE_DIR

DB_SOURCES = [
    "listado1.xml",
    "listado2.xml",
]

# Create your views here.
def index(request):
    print("FUNCIONA INDEX")
    comments = Comment.objects.all()
    context = {
        'comments': comments,
    }

    return render(request, "teveo_app/index.html", context)


def comentario(request):
    print("FUNCIONA COMENTARIO")
    return render(request, "teveo_app/comentario.html", {})


@csrf_exempt
def cameras(request):
    print("FUNCIONA CAMARAS")
    # si recibo un post, debo descargar dicho listado
    if request.method == "POST":
        print("ENTRO A POST")
        source = request.POST["source"]
        print(source)
        # debo obtener el path del archivo
        # print(BASE_DIR)
        source_path = os.path.join(BASE_DIR, "teveo_app/data_sources", source)
        print(source_path)
        cameras = utils.load_cameras_from_xml(source_path)
        print("CAMARITAS: ", cameras)

    camaras = Camera.objects.all()
    # Esta vista recibe el parámetro 'camaras'
    context = {
        'sources': DB_SOURCES,
        'cameras': camaras,
    }
    return render(request, "teveo_app/cameras.html", context)


def camera_detail(request, id_camera):
    print("FUNCIONA CAMERA_DETAIL")
    print(id_camera)

    try:
        camera = Camera.objects.get(id=id_camera)
        print(camera)
    except Camera.DoesNotExist:
        print("No existe la cámara")
        return HttpResponse("No existe la cámara")

    context = {
        'camera': camera,
    }
    return render(request, "teveo_app/camera_detail.html", context)


"""
def decide_option(request, comentario_camaras):
    print("FUNCIONA DECIDE_OPTION")
    if comentario_camaras == "camaras":
        print("ENTRO A CAMARAS")
        return cameras(request)
    elif comentario_camaras == "comentario":
        print("ENTRO A COMENTARIO")
        return comentario(request)
    else:
        print("ENTRO A ERROR")
        return HttpResponse("Error")
"""
