from django.db.models.signals import post_save
from .models import UserProfile
from courses.models import UserTopicProgress
from django.conf import settings
from django.dispatch import receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_progress_profile(sender, instance, created, **kwargs):
    if created:
        UserTopicProgress.objects.create(user=instance)

