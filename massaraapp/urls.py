# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('rooms/', home, name='home'),
    path('book-room/<int:room_id>/', book_room, name='book_room'),
    path('customer-bookings/', customer_bookings, name='customer_bookings'),
    path('staff-dashboard/', login_required(staff_dashboard, login_url='staff_login'), name='staff_dashboard'),
    path('register-room/', register_room, name='register_room'),
    path('', search, name='search'),
    path('search-results/', search_results, name='search_results'),
    path('staff-login/', staff_login, name='staff_login'),
    path('customer-login/', customer_login, name='customer_login'),
    path('staff-registration/', staff_registration, name='staff_registration'),
    path('customer-registration/', customer_registration, name='customer_registration'),
    path('release-room/<int:booking_id>/', release_room, name='release_room'),
    path('staff-logout/', staff_logout, name='staff_logout'),
    path('customer-logout/', customer_logout, name='customer_logout'),
    path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('restaurant', restaurant, name='restaurant'),
    path('legal', legal, name='legal'),
    path('contact', contact, name='contact'),
    path('gym', gym, name='gym'),
    path('blog', blog, name='blog'),
    path('about', about, name='about'),
    path('swimming',swimming,name='swimming'),
    path('cafe',cafe,name='cafe')
    
    
    
    
    
    # Add more URLs as needed
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)