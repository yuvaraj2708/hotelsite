# admin.py

from django.contrib import admin
from .models import CustomUser, Room, Booking

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type')
    search_fields = ('username', 'email')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'normal_price', 'season_price', 'available_count')
    search_fields = ('room_type',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'room', 'check_in_date', 'check_out_date', 'is_checked_out')
    list_filter = ('is_checked_out',)
    search_fields = ('customer__username', 'room__room_type', 'check_in_date', 'check_out_date')

# You can add more models if needed
