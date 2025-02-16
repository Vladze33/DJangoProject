from django.contrib import admin
from .models import Queue, Slot, Booking, Rating

admin.site.register(Queue)
admin.site.register(Slot)
admin.site.register(Booking)
admin.site.register(Rating)

class SlotInline(admin.TabularInline):
    model = Slot
    extra = 1

@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name',)
    inlines = [SlotInline]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    actions = ['mark_completed']
    
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
