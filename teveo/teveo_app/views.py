from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Camera, Comment
from . import utils
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from datetime import datetime

BASE_DIR = settings.BASE_DIR

DB_SOURCES = [
    "listado1.xml",
    "listado2.xml",
    "CCTV.kml",
]

# Create your views here.
def index(request):
    print("FUNCIONA INDEX")
    comments = Comment.objects.all().order_by('-date')
    print(comments)
    context = {
        'comments': comments,
    }

    return render(request, "teveo_app/index.html", context)


@csrf_exempt
def comentario(request):
    print("FUNCIONA COMENTARIO")

    # en el caso de que se rellene el formulario de comentario
    if request.method == "POST":
        print("ENTRO A POST")
        id_camera = request.POST["id_camera"]
        print(id_camera)
        comment_text = request.POST["comment_text"]
        print(comment_text)

        if not id_camera:
            return HttpResponse("ID de la cámara no específicado")

        # obtenemos la cámara correspondiente
        camera = Camera.objects.get(id=id_camera)

        # creamos y guardamos el comentario
        new_comment = Comment(
            id_camera=camera,
            date=datetime.now(),
            text=comment_text,
        )
        new_comment.save()

        return redirect("/teveo")

    id_camera = request.GET["id_camera"]
    print(id_camera)
    if not id_camera:
        return HttpResponse("ID de la cámara no específicado")
    camera = Camera.objects.get(id=id_camera)
    context = {
        'camera': camera,
        'current_date': datetime.now(),
    }
    return render(request, "teveo_app/comentario.html", context)


@csrf_exempt
def cameras(request):
    print("FUNCIONA CAMARAS")
    # si recibo un post, debo descargar dicho listado
    if request.method == "POST":
        print("ENTRO A POST")
        source = request.POST["source"]
        print(source)
        source_path = os.path.join(BASE_DIR, "teveo_app/data_sources", source)
        print(source_path)
        cameras = utils.load_cameras_from_xml(source_path)
        print("CAMARITAS: ", cameras)

    camaras = Camera.objects.all().order_by('-num_comments')
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


def camera_dyn(request, id_camera):
    print("FUNCIONA CAMERA_DYN")
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

    return render(request, "teveo_app/camera_detail_dyn.html", context)