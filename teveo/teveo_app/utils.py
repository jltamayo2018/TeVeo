import xml.etree.ElementTree as ET # para procesar archivos XML
from .models import Camera, DataSource

def extract_from_xml1(root):
    cameras = []

    for camara in root.findall("camara"):
        camera_id = camara.find("id").text
        img_camera = camara.find("src").text
        name = camara.find("lugar").text
        coordinates = camara.find("coordenadas").text.split(",")
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


def load_cameras_from_xml(data_source_path):
    tree = ET.parse(data_source_path) # cargamos el archivo XML
    root = tree.getroot() # obtenemos el elemento raíz del árbol xml

    # lista para almacenar las cámaras extraídas
    cameras = []
    if root.tag == "camaras":  # Formato del primer archivo XML (listado1.xml)
        cameras=extract_from_xml1(root)
    elif root.tag == "list":  # Formato del segundo archivo XML (listado2.xml)
        cameras=extract_from_xml2(root)
    return cameras
