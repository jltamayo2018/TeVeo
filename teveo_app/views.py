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


def index(request):
    # obtenemos todos los comentarios ordenados de la DB
    comments = Comment.objects.all().order_by('-date')
    # creamos el contexto para pasarselo a la plantilla
    context = {
        'pagina': "Principal",
        'comments': comments,
        'total_cameras': Camera.objects.count(),
        'total_comments': Comment.objects.count(),
    }
    # renderizamos (generamos) la plantilla
    return render(request, "index.html", context)


def download_image(url_imagen):
    """Download image and return it as bytes"""
    # me guardo en request la solicitud HTTP que se envia para obtener la imagen, a partir de la URL
    request = urllib.request.Request(url=url_imagen)
    try:
        # abro la URL y devuelvo la respuesta
        with urllib.request.urlopen(request) as response:
            # leo los datos de la respuesta y los almaceno
            image = response.read()
    except urllib.error.URLError as e:
        # si hay algun error devuelvo None y lo manejo luego
        return None
    return image


# función para manejar el método GET de comentario
def manage_comment_get(request):
    # obtenemos el id de la cámara
    id_camera = request.GET["id_camera"]
    if not id_camera:
        context = {
            'total_cameras': Camera.objects.count(),
            'total_comments': Comment.objects.count(),
            'motivo': "ID de la cámara no especificado",
        }
        return render(request, "error.html", context)
    try:
        # obtenemos la cámara si es posible
        camera = Camera.objects.get(id=id_camera)

        context = {
            'camera': camera,
            'current_date': datetime.now(),
            'total_cameras': Camera.objects.count(),
            'total_comments': Comment.objects.count(),
        }
        # renderizamos la página del comentario con el contexto
        return render(request, "comentario.html", context)

    except Camera.DoesNotExist:
        context = {
            'total_cameras': Camera.objects.count(),
            'total_comments': Comment.objects.count(),
            'motivo': "No existe la cámara solicitada",
        }
        return render(request, "error.html", context)


# función para manejar el método POST de comentario
def manage_comment_post(request):
    # extraemos los datos POST enviados en el formulario
    id_camera = request.POST["id_camera"]
    comment_text = request.POST["comment_text"]
    # verificamos si hay nombre de sesión, si no usaremos Anónimo
    if 'username' in request.session:
        username = request.session['username']
    else:
        username = "Anónimo"

    # verificamos que haya un id de la cámara, si no renderizamos la página de error
    if not id_camera:
        context = {
            'total_cameras': Camera.objects.count(),
            'total_comments': Comment.objects.count(),
            'motivo': "ID de la cámara no especificado",
        }
        return render(request, "error.html", context)

    # obtenemos la cámara correspondiente
    camera = Camera.objects.get(id=id_camera)
    # obtenemos su url
    image_url = camera.img_camera
    # descargamos la imagen
    image_bytes = download_image(image_url)
    if image_bytes:
        # codificamos la imagen en formato Base64
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
    # incrementamos el nº de comments de la cam y la guardamos
    camera.num_comments += 1
    camera.save()

    return redirect("/")


@csrf_exempt
def comentario(request):
    # en el caso de que se rellene el formulario de comentario
    if request.method == "POST":
        return manage_comment_post(request)

    # en el caso de que la petición sea GET
    elif request.method == "GET":
        return manage_comment_get(request)

    # cualquier otro caso -> error
    else:
        context = {
            'total_cameras': Camera.objects.count(),
            'total_comments': Comment.objects.count(),
            'motivo': "Método de la solicitud no aceptado",
        }
        return render(request, "error.html", context)


@csrf_exempt
def cameras(request):
    # si recibo un POST, debo descargar dicho listado
    if request.method == "POST":
        # obtenemos la fuente de datos
        source = request.POST["source"]
        # construimos la ruta del archivo
        source_path = os.path.join(BASE_DIR, "teveo_app/static/data_sources", source)
        # cargamos las cámaras desde el archivo xml
        utils.load_cameras_from_xml(source_path)

    # obtengo cámara aleatoria (solo si hay alguna cámara disponible)
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
    # si no hay cámaras, muestro la lista vacía
    else:
        context = {
            'pagina': "Cámaras",
            'sources': DB_SOURCES,
            'total_cameras': Camera.objects.count(),
            'total_comments': Comment.objects.count(),
        }

    return render(request, "cameras.html", context)


def like_camera(id_camera):
    # Incrementa en uno el número de likes de la cámara
    camera = Camera.objects.get(id=id_camera)
    camera.num_likes += 1
    camera.save()
    return redirect("/camaras")


@csrf_exempt
def camera_detail(request, id_camera):
    # si se pulsa el botón de like
    if request.method == "POST":
        return like_camera(id_camera)

    # obtenemos la cámara y mostramos la página
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
    # obtenemos la cámara y mostramos su página dinámica
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
        # convierte automáticamente los datos en la respuesta Json
        return JsonResponse(camera_data)
    except Camera.DoesNotExist:
        return JsonResponse({'Error': 'Cámara no encontrada'}, status=404)



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