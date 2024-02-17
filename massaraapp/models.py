# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Add this line
    
class Room(models.Model):
    ROOM_TYPES = [
        ('Studio', 'Studio'),
        ('Deluxe', 'Deluxe'),
        ('1BHK', '1BHK'),
        ('2BHK', '2BHK'),
        ('3BHK', '3BHK'),
    ]

    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    normal_price = models.DecimalField(max_digits=8, decimal_places=2)
    season_price = models.DecimalField(max_digits=8, decimal_places=2)
    available_count = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.room_type} - {self.available_count} available"

    class Meta:
        verbose_name_plural = 'Rooms'

class Booking(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    is_checked_out = models.BooleanField(default=False)
    is_released = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.customer.username} - Room {self.room.room_type}"

    def save(self, *args, **kwargs):
        # Ensure the room is marked as unavailable during the booked period
        self.room.available_count -= 1
        self.room.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Mark the room as available when a booking is deleted
        self.room.available_count += 1
        self.room.save()
        super().delete(*args, **kwargs)
