from django.test import TestCase, RequestFactory
from django.urls import reverse # para generar una URL a partir del nombre de la vista
from .models import Camera
from .views import index, cameras, help, settings, comentario, camera_dyn, camera_detail

# Create your tests here.
class CameraTestCase(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas
        Camera.objects.create(name='test_name')

    def test_model_creation(self):
        obj = Camera.objects.get(name='test_name')
        self.assertEqual(obj.name, 'test_name')

class TestExtremoToExtremo(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def testIndex(self):
        # Crea una solicitud GET para la vista index
        request = self.factory.get(reverse('index'))
        response = index(request)
        # Verifica que la respuesta tenga un código 200 (OK)
        self.assertEqual(response.status_code, 200)

    def testSettings(self):
        # Crea una solicitud GET para la vista settings
        request = self.factory.get(reverse('settings'))
        response = settings(request)
        # Verifica que la respuesta tenga un código 200 (OK)
        self.assertEqual(response.status_code, 200)

    def testAyuda(self):
        # Crea una solicitud GET para la vista help
        request = self.factory.get(reverse('help'))
        response = help(request)
        # Verifica que la respuesta tenga un código 200 (OK)
        self.assertEqual(response.status_code, 200)