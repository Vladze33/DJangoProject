from django.contrib import admin
from .models import Queue, Slot, Booking, Rating

admin.site.register(Queue)
admin.site.register(Slot)
admin.site.register(Booking)
admin.site.register(Rating)
