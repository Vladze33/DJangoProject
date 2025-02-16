from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking, Rating

@receiver(post_save, sender=Booking)
def create_rating(sender, instance, created, **kwargs):
    if instance.status == 'completed' and not hasattr(instance, 'rating'):
        Rating.objects.create(booking=instance, rating=5)  # Дефолтная оценка
