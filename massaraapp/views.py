# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import CustomUser, Room, Booking
from .forms import BookingForm,RoomRegistrationForm
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from .forms import CustomerRegistrationForm, StaffRegistrationForm


def home(request):
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})

@login_required
def book_room(request, room_id):
    room = Room.objects.get(pk=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.room = room
            booking.save()
            messages.success(request, 'Room booked successfully!')
            return redirect('customer_bookings')
    else:
        form = BookingForm()
    request.session['booking_success'] = True
    return render(request, 'book_room.html', {'form': form, 'room': room})

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)

    if booking.is_checked_out:
        messages.error(request, 'Cannot cancel a checked-out booking.')
    else:
        # Mark the booking as canceled
        booking.is_canceled = True
        booking.save()
        messages.success(request, 'Booking canceled successfully.')

    return redirect('customer_bookings')

def customer_bookings(request):
    bookings = Booking.objects.filter(customer=request.user)
    user_details = request.user
    return render(request, 'customer_bookings.html', {'bookings': bookings, 'user_details': user_details})

@login_required
def staff_dashboard(request):
    bookings = Booking.objects.all()
    return render(request, 'staff_dashboard.html', {'bookings': bookings})

@login_required
def register_room(request):
    if request.method == 'POST':
        form = RoomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room registered successfully!')
            return redirect('staff_dashboard')  # Redirect to staff dashboard
    else:
        form = RoomRegistrationForm()

    return render(request, 'register_room.html', {'form': form})



def search(request):
    return render(request, 'search.html')

def search_results(request):
    if request.method == 'GET':
        # Extract search parameters
        room_type = request.GET.get('room-type')

        # Create a query to filter rooms based on available_count
        query = Q(available_count__gte=1)

        # Optionally, include room_type in the query
        if room_type:
            query &= Q(room_type=room_type)

        # Filter rooms based on the query
        available_rooms = Room.objects.filter(query).distinct()

        print("Room Type:", room_type)
        print("Query:", available_rooms.query)

        return render(request, 'search_results.html', {'available_rooms': available_rooms})

    # If no valid search parameters, render the search page
    return render(request, 'search.html')




def staff_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.user_type == 'staff':
            login(request, user)
            return redirect('staff_dashboard')  # Redirect to staff dashboard
        else:
            # Handle invalid login credentials
            return render(request, 'staff_login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'staff_login.html')

def customer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.user_type == 'customer':
            login(request, user)
            return redirect('search')  # Redirect to customer dashboard
        else:
            # Handle invalid login credentials
            return render(request, 'customer_login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'customer_login.html')


def customer_registration(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('customer_login')  # Redirect to customer dashboard page
    else:
        form = CustomerRegistrationForm()
    request.session['booking_success'] = True
    return render(request, 'customer_registration.html', {'form': form})

def staff_registration(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('staff_dashboard')  # Redirect to staff dashboard page
    else:
        form = StaffRegistrationForm()

    return render(request, 'staff_registration.html', {'form': form})

def staff_logout(request):
    logout(request)
    return redirect('staff_login')  # Redirect to login page

def customer_logout(request):
    logout(request)
    return redirect('customer_login')  # Redirect to login page

@login_required
def release_room(request, booking_id):
    print(f"Release Room View - Booking ID: {booking_id}")
    booking = get_object_or_404(Booking, id=booking_id)

    # Check if the user has permission to release the room
    if not request.user.is_staff and not booking.is_checked_out and not booking.is_released:
        # Mark the booking as released and checked out
        booking.is_released = True
        booking.is_checked_out = True
        booking.save()
        messages.success(request, 'Room released successfully.')
    else:
        messages.error(request, 'Unable to release the room.')
    
    return redirect('staff_dashboard')


def restaurant(request):
    return render(request,'restaurant.html')

def contact(request):
    return render(request,"contact.html")

def gym(request):
    return render(request,"gym.html")

def legal(request):
    return render(request,"legal.html")

def blog(request):
    return render(request,"blog.html")

def about(request):
    return render(request,"about.html")

def swimming(request):
    return render(request,"swimming.html")

def cafe(request):
    return render(request,"cafe.html")