from django.urls import re_path

from .views import get_user_images, get_expiring_link, upload_image

urlpatterns = [
    re_path(r'upload', upload_image),
    re_path(r'all', get_user_images),
    re_path(r'expiring/', get_expiring_link),
]
