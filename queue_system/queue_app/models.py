from django.db import models
from django.contrib.auth.models import User


class Queue(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Slot(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.queue.name} - {self.start_time} to {self.end_time}"


class Booking(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.slot}"


class Rating(models.Model):
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=[(1, 'Очень плохо'), (2, 'Плохо'), (3, 'Нормально'), (4, 'Хорошо'), (5, 'Отлично')]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('booking', 'user')

    def __str__(self):
        return f"Rating {self.rating} from {self.user.username} for {self.booking}"
