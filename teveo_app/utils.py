import xml.etree.ElementTree as ET # para procesar archivos XML
from .models import Camera
import re

# Definimos el espacio de nombres utilizado en los archivos KML para referirse a elementos dentro de estos archivos.
KML_NAMESPACE = {"kml": "http://earth.google.com/kml/2.2"}

def extract_from_xml1(root):
    cameras = []

    # encontramos los elementos 'camara' dentro del xml
    for camara in root.findall("camara"):
        # obtenemos los subelementos que nos interesan
        camera_id = camara.find("id").text
        img_camera = camara.find("src").text
        name = camara.find("lugar").text
        coordinates = camara.find("coordenadas").text.split(",")
        latitude = float(coordinates[1])
        longitude = float(coordinates[0])

        # Creamos o actualizamos la cámara si ya existe
        camera, created = Camera.objects.update_or_create(
            id=camera_id,
            defaults={
                "img_camera": img_camera,
                "name": name,
                "latitude": latitude,
                "longitude": longitude,
            }
        )
        cameras.append(camera)

    return cameras


def extract_from_xml2(root):
    cameras =[]

    for cam in root.findall("cam"):
        camera_id = cam.get("id")
        img_camera = cam.find("url").text
        info = cam.find("info").text
        latitude = float(cam.find("place/latitude").text)
        longitude = float(cam.find("place/longitude").text)

        # Crear o actualizar la cámara
        camera, created = Camera.objects.update_or_create(
            id=camera_id,
            defaults={
                "img_camera": img_camera,
                "name": info,
                "latitude": latitude,
                "longitude": longitude,
            }
        )
        cameras.append(camera)

    return cameras


def extract_from_kml(root, namespace):
    cameras = []

    for placemark in root.findall(".//kml:Placemark", namespace):
        # Obtener la descripción para obtener la URL de la imagen
        description = placemark.find("kml:description", namespace).text
        # Extraer la URL de la imagen usando una expresión regular

        img_camera_match = re.search(r'src=([^ ]+)', description)
        img_camera = img_camera_match.group(1) if img_camera_match else None

        # Obtener la información básica de la cámara
        camera_id = placemark.find(".//kml:Data[@name='Numero']/kml:Value", namespace).text
        name = placemark.find(".//kml:Data[@name='Nombre']/kml:Value", namespace).text
        coordinates = placemark.find(".//kml:Point/kml:coordinates", namespace).text.split(",")
        latitude = float(coordinates[1])
        longitude = float(coordinates[0])

        # Crear o actualizar la cámara
        camera, created = Camera.objects.update_or_create(
            id=camera_id,
            defaults={
                "img_camera": img_camera,
                "name": name,
                "latitude": latitude,
                "longitude": longitude,
            }
        )
        cameras.append(camera)

    return cameras


def load_cameras_from_xml(data_source_path):
    # cargamos el archivo XML para analizarlo y cargarlo, tree representa la estructura completa del XML
    tree = ET.parse(data_source_path)
    # obtenemos el elemento raíz del árbol xml
    root = tree.getroot()
    # guardamos el nombre de la etiqueta raiz del XML como una cadena de texto
    root_tag = root.tag.split("}")[-1]
    print("ROOT_TAG:", root_tag)

    # lista para almacenar las cámaras extraídas
    cameras = []
    # Formato del primer archivo XML (listado1.xml)
    if root_tag == "camaras":
        cameras=extract_from_xml1(root)
    # (listado2.xml)
    elif root_tag == "list":
        cameras=extract_from_xml2(root)
    # CCTV.kml
    elif root_tag == "kml":
        cameras=extract_from_kml(root, KML_NAMESPACE)

    return cameras
