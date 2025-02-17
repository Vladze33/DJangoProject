from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from .models import Queue, Slot, Booking, Rating
from .forms import BookingForm, RatingForm, RegisterForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone



def queue_list(request):
    queues = Queue.objects.all()
    return render(request, 'queue_app/queue_list.html', {'queues': queues})


@login_required
def slot_list(request, queue_id):
    queue = get_object_or_404(Queue, id=queue_id)
    if is_admin(request.user):  # Проверяем, является ли пользователь администратором
        slots = Slot.objects.filter(queue=queue)  # Администратор видит все слоты
    else:
        slots = Slot.objects.filter(queue=queue, is_available=True)  # Обычный пользователь видит только доступные
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
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    now = timezone.localtime(timezone.now())
    for booking in bookings:
        end_time = timezone.localtime(booking.slot.end_time)
        booking.slot.can_rate = end_time < now
    return render(request, 'queue_app/user_bookings.html', {'bookings': bookings, 'now': now})


@login_required
def rate_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    try:
        rating = Rating.objects.get(booking=booking, user=request.user)
    except Rating.DoesNotExist:
        rating = None

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.booking = booking
            rating.user = request.user
            rating.save()
            return redirect('user_bookings')
    else:
        form = RatingForm(instance=rating)

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


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def call_next_user(request, queue_name, start_time):
    if request.method == 'POST':
        slot = get_object_or_404(Slot, queue__name=queue_name, start_time=start_time)
        next_booking = Booking.objects.filter(slot=slot, notified=False).first()

        if next_booking:
            # Отправка письма
            send_mail(
                subject='Ваша очередь подошла',
                message=f'Здравствуйте, {next_booking.user.username}! Ваша очередь подошла. Пожалуйста, подойдите к стойке обслуживания.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[next_booking.user.email],
            )

            # Помечаем, что уведомление отправлено
            next_booking.notified = True
            next_booking.save()
            messages.success(request, f"Пользователь {next_booking.user.username} был успешно вызван.")
        else:
            messages.info(request, "В очереди нет ожидающих пользователей.")

    return redirect('slot_detail', queue_name=queue_name, start_time=start_time)


@login_required
def slot_detail(request, queue_name, start_time):
    slot = get_object_or_404(Slot, queue__name=queue_name, start_time=start_time)
    bookings = Booking.objects.filter(slot=slot)
    next_booking = Booking.objects.filter(slot=slot, notified=False).first()
    is_admin_user = is_admin(request.user)
    context = {'slot': slot, 'bookings': bookings, 'next_booking': next_booking, 'is_admin': is_admin_user}
    return render(request, 'queue_app/slot_detail.html', context)
