from django.urls import re_path

from .views import upload_image

urlpatterns = [
    re_path(r'', upload_image)
]
