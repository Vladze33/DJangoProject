from django.urls import path
from . import views

urlpatterns = [
    path('', views.queue_list, name='queue_list'),
    path('queue/<int:queue_id>/', views.slot_list, name='slot_list'),
    path('book/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('rate/<int:booking_id>/', views.rate_booking, name='rate_booking'),
    path('queue/<str:queue_name>/', views.slot_list, name='slot_list'),
    path('queue/<str:queue_name>/<str:start_time>/', views.slot_detail, name='slot_detail'),
    path('queue/<str:queue_name>/<str:start_time>/call_next/', views.call_next_user, name='call_next_user'),
    path('my-bookings/', views.user_bookings, name='user_bookings'),
    path('rate-booking/<int:booking_id>/', views.rate_booking, name='rate_booking'),
]
