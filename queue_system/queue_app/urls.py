from django.urls import path
from . import views

urlpatterns = [
    path('', views.queue_list, name='queue_list'),
    path('queue/<int:queue_id>/', views.slot_list, name='slot_list'),
    path('book/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('rate/<int:booking_id>/', views.rate_booking, name='rate_booking'),
]
