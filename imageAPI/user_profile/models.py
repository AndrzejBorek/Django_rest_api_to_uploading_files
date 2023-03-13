from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from account_tier.models import AccountTier


User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='user_profile')
    account_tier = models.ForeignKey(AccountTier, on_delete=models.SET_NULL, null=True, blank=True)
    images = models.ManyToManyField('image.Image', blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        instance.user_profile.save()
