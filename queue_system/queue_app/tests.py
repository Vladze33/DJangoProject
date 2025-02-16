from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from .models import Queue, Slot, Booking


class QueueTest(TestCase):
    def test_queue_creation(self):
        queue = Queue.objects.create(name="Test", status="active")
        self.assertEqual(queue.status, "active")


class BookingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.queue = Queue.objects.create(name="Test")
        self.slot = Slot.objects.create(queue=self.queue, start_time="2025-01-01 10:00", end_time="2025-01-01 11:00")

    def test_booking_status(self):
        booking = Booking.objects.create(slot=self.slot, user=self.user)
        self.assertEqual(booking.status, "waiting")
