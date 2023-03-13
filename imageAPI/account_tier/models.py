from django.db import models
from django.db.models import JSONField


class AccountTier(models.Model):
    name = models.CharField(max_length=20, default='account tier')
    thumbnail_sizes = JSONField(default=list)
    link_to_original = models.BooleanField(default=False)
    expiring_links = models.BooleanField(default=False)

    def __str__(self):
        return self.name
