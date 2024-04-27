from django.shortcuts import render
from django.http import HttpResponse
from .models import Camera
from .models import Comment

# Create your views here.
def index(request):
    print("FUNCIONA INDEX")
    comments = Comment.objects.all()
    context = {
        'comments': comments,
    }

    return render(request, "teveo_app/index.html", context)

    #return render(request, "teveo_app/index.html")

def cameras(request):
    print("FUNCIONA CAMARAS")
    camaras = Camera.objects.all()
    # Esta vista recibe el parámetro 'camaras'
    context = {
        'cameras': camaras,
    }
    return render(request, "teveo_app/cameras.html", context)

def comentario(request):
    print("FUNCIONA COMENTARIO")
    return render(request, "teveo_app/comentario.html", {})

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
