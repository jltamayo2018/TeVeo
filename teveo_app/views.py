from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Camera, Comment
from . import utils
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from datetime import datetime
import urllib.request
import base64
import random
from django.contrib.auth import logout
from django.http import JsonResponse

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
        'pagina': "Principal",
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
        if 'username' in request.session:
            username = request.session['username']
        else:
            username = "Anónimo"

        if not id_camera:
            return HttpResponse("ID de la cámara no específicado")

        # obtenemos la cámara correspondiente
        camera = Camera.objects.get(id=id_camera)

        image_url = camera.img_camera
        image_bytes = download_image(image_url)
        if image_bytes:
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        if image_bytes == None:
            image_base64 = None
        # creamos y guardamos el comentario
        new_comment = Comment(
            id_camera=camera,
            date=datetime.now(),
            text=comment_text,
            image=image_base64,
            author=username,
        )
        new_comment.save()
        camera.num_comments += 1
        camera.save()

        return redirect("/")

    id_camera = request.GET["id_camera"]
    if not id_camera:
        return HttpResponse("ID de la cámara no específicado")
    try:
        camera = Camera.objects.get(id=id_camera)
    except Camera.DoesNotExist:
        context = {
            'total_cameras': Camera.objects.count(),
            'total_comments': Comment.objects.count(),
            'motivo': "No existe la cámara solicitada",
        }
        return render(request, "error.html", context)
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
        camaras = utils.load_cameras_from_xml(source_path)

    # obtengo cámara aleatoria
    if (Camera.objects.count() > 0):
        random_camera = random.choice(Camera.objects.all())

        camaras = Camera.objects.all().order_by('-num_comments')
        context = {
            'pagina': "Cámaras",
            'sources': DB_SOURCES,
            'cameras': camaras,
            'total_cameras': Camera.objects.count(),
            'total_comments': Comment.objects.count(),
            'random_camera': random_camera,
        }
    else:
        context = {
            'pagina': "Cámaras",
            'sources': DB_SOURCES,
            'total_cameras': Camera.objects.count(),
            'total_comments': Comment.objects.count(),
        }

    return render(request, "cameras.html", context)


def like_camera(id_camera):
    """Incrementa en uno el número de likes de la cámara"""
    camera = Camera.objects.get(id=id_camera)
    camera.num_likes += 1
    camera.save()


@csrf_exempt
def camera_detail(request, id_camera):
    if request.method == "POST":
        like_camera(id_camera)

        return redirect("/camaras")

    try:
        camera = Camera.objects.get(id=id_camera)
    except Camera.DoesNotExist:
        context = {
            'total_cameras': Camera.objects.count(),
            'total_comments': Comment.objects.count(),
            'motivo': "No existe la cámara solicitada",
        }
        return render(request, "error.html", context)

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
        context = {
            'total_cameras': Camera.objects.count(),
            'total_comments': Comment.objects.count(),
            'motivo': "No existe la cámara solicitada",
        }
        return render(request, "error.html", context)

    context = {
        'camera': camera,
        'total_cameras': Camera.objects.count(),
        'total_comments': Comment.objects.count(),
        'comments_for_this_camera': Comment.objects.filter(id_camera=camera).order_by('-date'),
    }

    return render(request, "camera_detail_dyn.html", context)


def camera_json(request, id_camera):
    try:
        camera = Camera.objects.get(id=id_camera)
        camera_data = {
            'id': camera.id,
            'name': camera.name,
            'latitude': camera.latitude,
            'longitude': camera.longitude,
            'num_comments': camera.num_comments,
        }
        return JsonResponse(camera_data)
    except Camera.DoesNotExist:
        return JsonResponse({'error': 'Cámara no encontrada'}, status=404)



def help(request):
    context = {
        'pagina': "Ayuda",
        'total_cameras': Camera.objects.count(),
        'total_comments': Comment.objects.count(),
    }

    return render(request, "help.html", context)


@csrf_exempt
def settings(request):
    if request.method == "POST":
        if "save_username" in request.POST:
            new_username = request.POST.get("username")
            # Almacena el nombre del comentador en la sesión del usuario
            request.session['username'] = new_username

        elif "save_appearance" in request.POST:
            font_size = request.POST.get("font_size")
            font_type = request.POST.get("font_type")
            # Guarda el tamaño y tipo de fuente en la sesión del usuario
            request.session['font_size'] = font_size
            request.session['font_type'] = font_type

        elif "authorize-button" in request.POST:
            if request.session.session_key != None:
                dominio = request.get_host()
                cookie = request.session.session_key
                enlace = f"http://{dominio}/cambio/{cookie}"
                auth_link = {
                    'auth_link': enlace,
                }
                return JsonResponse(auth_link)
            else:
                context = {
                    'pagina': "Configuración",
                    'session_key': "No",
                    'total_cameras': Camera.objects.count(),
                    'total_comments': Comment.objects.count(),
                }

                return render(request, "settings.html", context)

        else:
            logout(request)
            # Almacena el nombre del comentador en la sesión del usuario


    context = {
        'pagina': "Configuración",
        'total_cameras': Camera.objects.count(),
        'total_comments': Comment.objects.count(),
    }

    return render(request, "settings.html", context)


def cambio(request, cookie):
    response = redirect('/') # Función para redirigir a la págin principal
    # Establezco la cookie
    # set_cookie es el método para establecer la cookie en la respuesta de sesión
    response.set_cookie(
        key='sessionid', # nombre de la cookie de sesión
        value=cookie, # valor de la cookie (especificado como parámetro en el enlace)
    )
    return response