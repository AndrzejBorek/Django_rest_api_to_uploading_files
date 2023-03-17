from django.contrib.auth.models import User
from django.db import models
from django.db.models import JSONField
from rest_framework import serializers
from django.core.exceptions import ValidationError


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail_sizes = JSONField(default=list, blank=True)
    name = models.CharField(max_length=50)
    image_paths = JSONField(default=list, blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk is None and Image.objects.filter(name=self.name, user=self.user).exists():
            raise ValidationError("An image with this name already exists for this user.")
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'image'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['name']
