from django.db import models

# Create your models here.
class Camera(models.Model):
    id = models.CharField(max_length = 200, primary_key=True)
    name = models.CharField(max_length = 200, default="")
    latitude = models.CharField(max_length = 200, default="", null=True, blank=True)
    longitude = models.CharField(max_length = 200, default="", null=True, blank=True)
    # message = models.CharField(max_length = 200, default="")

    #def __str__(self):
    #    return self.id


class Comment(models.Model):
    id_camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    date = models.DateTimeField() #(auto_now_add=True)
    text = models.CharField(max_length=200, default="")
    #img_camera = models.ImageField(upload_to='images/', blank=True, null=True)
