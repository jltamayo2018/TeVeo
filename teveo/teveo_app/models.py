from django.db import models

# Create your models here.


class DataSource(models.Model):
    name = models.CharField(max_length=200)
    file_path = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Camera(models.Model):
    id = models.CharField(max_length = 200, primary_key=True)
    name = models.CharField(max_length = 200, default="")
    latitude = models.CharField(max_length = 200, default="", null=True, blank=True)
    longitude = models.CharField(max_length = 200, default="", null=True, blank=True)
    num_comements = models.IntegerField(default=0)
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    id_camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    date = models.DateTimeField() #(auto_now_add=True)
    text = models.CharField(max_length=200, default="")
    #img_camera = models.ImageField(upload_to='images/', blank=True, null=True)
