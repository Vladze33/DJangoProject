from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Queue, Slot, Booking, Rating
from .forms import BookingForm, RatingForm, RegisterForm
from django.contrib.auth import login


def queue_list(request):
    queues = Queue.objects.all()
    return render(request, 'queue_app/queue_list.html', {'queues': queues})


@login_required
def slot_list(request, queue_id):
    queue = get_object_or_404(Queue, id=queue_id)
    slots = Slot.objects.filter(queue=queue, is_available=True)
    return render(request, 'queue_app/slot_list.html', {'queue': queue, 'slots': slots})


@login_required
def book_slot(request, slot_id):
    slot = get_object_or_404(Slot, id=slot_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            slot.is_available = False
            slot.save()
            send_mail(
                'Booking Confirmation',
                f'You have successfully booked a slot from {slot.start_time} to {slot.end_time}.',
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )
            return redirect('queue_list')
    else:
        form = BookingForm(initial={'slot': slot})
    return render(request, 'queue_app/book_slot.html', {'form': form, 'slot': slot})


@login_required
def rate_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.booking = booking
            rating.save()
            return redirect('queue_list')
    else:
        form = RatingForm()
    return render(request, 'queue_app/rate_booking.html', {'form': form, 'booking': booking})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('queue_list')  # Перенаправление после регистрации
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
