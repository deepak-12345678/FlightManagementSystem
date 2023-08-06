from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', FlightListView, name="flightlist"),
    path('seats/', GetSeatListView, name="seatlist"),
    # path('book/', BookSeatView, name="book"),
    path('bookings/', BookingListView, name="bookinglist"),
    path('booking/', GetBookingView, name="bookingView"),
    path("cancellations/", CancellationListView, name="cancellationView"),
    path("email/", EmailListView, name="emailView"),
    path("sms/", SmsListView, name="smsView"),
    path('cancel/', CancelBookingView, name="cancel"),
    path('search/', SearchFlightView, name='search')   
]