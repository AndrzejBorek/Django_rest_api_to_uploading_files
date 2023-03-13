from django.contrib.auth.models import User
from django.db import models


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    image_path = models.CharField(max_length=255)
    upload_time = models.DateTimeField(auto_now_add=True)
