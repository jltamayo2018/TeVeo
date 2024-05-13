from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Camera, Comment
from . import utils
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from datetime import datetime
import urllib.request
import requests
import base64
import random
from django.contrib.auth.decorators import login_required

BASE_DIR = settings.BASE_DIR

DB_SOURCES = [
    "listado1.xml",
    "listado2.xml",
    "CCTV.kml",
]

# Create your views here.
def index(request):
    comments = Comment.objects.all().order_by('-date')
    context = {
        'comments': comments,
        'total_cameras': Camera.objects.count(),
        'total_comments': Comment.objects.count(),
    }

    return render(request, "index.html", context)


def download_image(url_imagen):
    """Download image and return it as bytes"""
    request = urllib.request.Request(url=url_imagen)
    try:
        with urllib.request.urlopen(request) as response:
            image = response.read()
    except urllib.error.URLError as e:
        return None
    return image


@csrf_exempt
def comentario(request):
    # en el caso de que se rellene el formulario de comentario
    if request.method == "POST":
        id_camera = request.POST["id_camera"]
        comment_text = request.POST["comment_text"]

        if not id_camera:
            return HttpResponse("ID de la cámara no específicado")

        # obtenemos la cámara correspondiente
        camera = Camera.objects.get(id=id_camera)

        image_url = camera.img_camera
        response = requests.get(image_url)
        if response.status_code == 200:
            image_bytes = download_image(image_url)
            if image_bytes:
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        # creamos y guardamos el comentario
        new_comment = Comment(
            id_camera=camera,
            date=datetime.now(),
            text=comment_text,
            image=image_base64,
        )
        new_comment.save()

        camera.num_comments += 1
        camera.save()

        return redirect("/")

    id_camera = request.GET["id_camera"]
    if not id_camera:
        return HttpResponse("ID de la cámara no específicado")
    camera = Camera.objects.get(id=id_camera)
    context = {
        'camera': camera,
        'current_date': datetime.now(),
        'total_cameras': Camera.objects.count(),
        'total_comments': Comment.objects.count(),
    }
    return render(request, "comentario.html", context)


@csrf_exempt
def cameras(request):
    # si recibo un post, debo descargar dicho listado
    if request.method == "POST":
        source = request.POST["source"]
        source_path = os.path.join(BASE_DIR, "teveo_app/static/data_sources", source)
        cameras = utils.load_cameras_from_xml(source_path)

    # obtengo cámara aleatoria
    random_camera = random.choice(Camera.objects.all())

    camaras = Camera.objects.all().order_by('-num_comments')
    context = {
        'sources': DB_SOURCES,
        'cameras': camaras,
        'total_cameras': Camera.objects.count(),
        'total_comments': Comment.objects.count(),
        'random_camera': random_camera,
    }
    return render(request, "cameras.html", context)


def camera_detail(request, id_camera):
    try:
        camera = Camera.objects.get(id=id_camera)
    except Camera.DoesNotExist:
        return HttpResponse("No existe la cámara")

    context = {
        'camera': camera,
        'total_cameras': Camera.objects.count(),
        'total_comments': Comment.objects.count(),
        'comments_for_this_camera': Comment.objects.filter(id_camera=camera).order_by('-date'),
    }
    return render(request, "camera_detail.html", context)


def camera_dyn(request, id_camera):

    try:
        camera = Camera.objects.get(id=id_camera)
    except Camera.DoesNotExist:
        return HttpResponse("No existe la cámara")

    context = {
        'camera': camera,
        'total_cameras': Camera.objects.count(),
        'total_comments': Comment.objects.count(),
        'comments_for_this_camera': Comment.objects.filter(id_camera=camera).order_by('-date'),
    }

    return render(request, "camera_detail_dyn.html", context)


def help(request):
    context = {
        'total_cameras': Camera.objects.count(),
        'total_comments': Comment.objects.count(),
    }

    return render(request, "help.html", context)


@csrf_exempt
def settings(request):
    if request.method == "POST":
        print("ENTRO A POST")
        if "save_username" in request.POST:
            print("ENTRO A username")
            
        if "save_appearance" in request.POST:
            print("ENTRO A appearance")

    context = {
        'total_cameras': Camera.objects.count(),
        'total_comments': Comment.objects.count(),
    }

    return render(request, "settings.html", context)