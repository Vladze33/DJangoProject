from django.contrib import admin
from .models import Queue, Slot, Booking, Rating


# Регистрация модели Queue
@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


# Регистрация модели Slot
@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('queue', 'start_time', 'end_time', 'is_available')


# Регистрация модели Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('slot', 'user', 'created_at', 'notified')


# Регистрация модели Rating
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating', 'comment', 'created_at')