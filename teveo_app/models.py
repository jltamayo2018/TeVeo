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
    num_comments = models.IntegerField(default=0)
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, null=True, blank=True)
    img_camera = models.CharField(max_length = 200, default="", null=True, blank=True)
    num_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Comment(models.Model):
    id_camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    date = models.DateTimeField() #(auto_now_add=True)
    text = models.CharField(max_length=200, default="")
    image = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=200, default="Anónimo")

    def __str__(self):
        return self.text