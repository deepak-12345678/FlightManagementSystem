from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import connection
# import mysql.connector 
from ticketBook import keyconfig as senv
# from mysql.connector import Error, connect
# Create your views here.
from django.conf import settings
from django.core.mail import send_mail

def get_flight_data(queryset):
    data = []
    for flight in queryset:
        cursor = connection.cursor()
        cursor.execute("select cost from price where seat_type = 'Economy' and flight_id=%s", [flight.pk])
        ecomony = cursor.fetchone()[0]
        cursor.execute("select cost from price where seat_type = 'Business' and flight_id=%s", [flight.pk])
        business = cursor.fetchone()[0]
        data_small = {
            "flight_id":flight.pk,
            "name":flight.name,
            "source":flight.source,
            "destination":flight.destination,
            "start_time":flight.start_time,
            "end_time":flight.end_time,
            "economy":ecomony,
            "business":business,
        }
        data.append(data_small)
    return data

def get_seat_data(queryset, request=None):
    data = []
    cursor = connection.cursor()
    for seat in queryset:
        price = 0
        print(seat.seat_type, seat.flight.pk)
        cursor.execute("select cost from price where seat_type = %s and flight_id=%s", [seat.seat_type, seat.flight.pk])
        try:
            price = cursor.fetchone()[0]
            if not price:
                price = 0
        except:
            price =0
        data_small = {
            "id":seat.pk,
            "name":seat.name,
            "price":price,
            "type":seat.seat_type,
            "is_booked":False,
        }
        booking = Booking.objects.raw("SELECT * FROM bookings WHERE bookings.seat_id = %s AND bookings.status != 'Completed' AND bookings.status != 'Cancelled'", [seat.pk])
        if booking:
            data_small["is_booked"] = True
        if request:
            booking = Booking.objects.raw("SELECT * FROM bookings WHERE bookings.seat_id = %s AND bookings.status != 'Completed' AND bookings.status != 'Cancelled' AND bookings.user_id = %s", [seat.pk, request.user.pk])
            if booking:
                data_small["booking_id"] = booking[0].pk
                data_small["status"] = booking[0].status
                data_small["booked_by_you"] = True
            else:
                data_small["booked_by_you"] = False

        data.append(data_small)
    return data

def get_booking_data(queryset):
    data = []
    for booking in queryset:
        seat = Seat.objects.raw(f'SELECT * FROM seats WHERE seats.seat_id = {booking.seat.pk}')[0]
        data_small = {
            "id":booking.pk,
            "seat":seat.name,
            "status":booking.status,
            "created_at":booking.created_at,
            "seat_id":seat.pk,
        }
        data.append(data_small)
    return data

def get_single_booking_data(booking):
    seat = Seat.objects.raw(f'SELECT * FROM seats WHERE seat_id = {booking.seat.pk}')[0]
    data = {
        "id":booking.pk,
        "seat":seat.name,
        "status":booking.status,
        "created_at":booking.created_at,
        "seat_id":seat.pk,
    }
    return data

def get_cancellation_data(queryset):
    data = []
    for cancellation in queryset:
        booking = Booking.objects.raw(f'SELECT * FROM bookings WHERE bookings.booking_id = {cancellation.booking.pk}')[0]
        seat = Seat.objects.raw(f'SELECT * FROM seats WHERE seats.seat_id = {booking.seat.pk}')[0]
        flight = Flight.objects.raw(f'SELECT * FROM flights WHERE flights.flight_id = {seat.flight.pk}')[0]
        data_small = {
            "booking_id":cancellation.booking.pk,
            "created_at":cancellation.created_at,
            "seat":seat.seat_type + " " + str(seat.pk%8),
            "flight":flight.name,
            "reason":cancellation.reason,

        }
        data.append(data_small)
    return data

def get_email_data(queryset):
    data = []
    for email in queryset:
        data_small = {
            "id":email.pk,
            "subject":email.subject,
            "body":email.body,
            "created_at":email.created_at,
        }
        data.append(data_small)
    return data

def get_sms_data(queryset):
    data = []
    for sms in queryset:
        data_small = {
            "id":sms.pk,
            "body":sms.body,
            "created_at":sms.created_at,
        }
        data.append(data_small)
    return data

def FlightListView(request):
    if(request.method.lower() == "post"):
        # current_user = UserC.objects.filter(email=request.POST.get("name"), password=request.POST.get("password")).first()
        current_user = UserC.objects.raw(f'SELECT * FROM passengers WHERE (passengers.email = "{request.POST.get("name")}" AND passengers.password =  "{request.POST.get("password")}")')[0]
        if not current_user:
            return redirect("login")
        login(request, current_user)
        # request.user = current_user
    query = f"select * from flights where 1=1"
    print(request.method)
    if request.method == "GET":
        if request.GET.get('destination'):
            query += f" and destination = '{request.GET.get('destination')}'"
        if request.GET.get('source'):
            query += f" and source = '{request.GET.get('source')}'"
        if request.GET.get('date'):
            query += f" and CAST(start_time AS DATE) = '{request.GET.get('date')}'"
        print(request.GET)
    flights = Flight.objects.raw(query)
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "flightlist.html", context={"data":get_flight_data(flights), "destination":request.GET.get('destination'), "source":request.GET.get('source')})


def SearchFlightView(request):
    if(request.method.lower() == "post"):
        # current_user = UserC.objects.filter(email=request.POST.get("name"), password=request.POST.get("password")).first()
        try:
            current_user = UserC.objects.raw(f'SELECT * FROM passengers WHERE (passengers.email = "{request.POST.get("name")}" AND passengers.password =  "{request.POST.get("password")}")')[0]
        except IndexError as e:
            current_user = None
        if not current_user:
            return redirect("login")
        login(request, current_user)
        # request.user = current_user
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "searchbox.html", context={"destination":request.POST.get('destination'), "source":request.POST.get('source')})


def GetSeatListView(request):
    if not request.user.is_authenticated:
        return redirect("login")
    already=False
    available = False
    print(request.user, request.method)
    if request.method=="POST":
        seat = Seat.objects.raw(f"select * from seats where seat_id = {request.POST.get('seat_id')}")[0]
        cursor = connection.cursor()
        booking = Booking.objects.raw(f"select * from bookings where seat_id = {seat.pk} and status != 'Completed' and status != 'Cancelled' for update ")
        if booking:
            already=True
        else:
            try:
                cursor.execute(f"call insert_booking({seat.pk}, '{request.user.pk}')")
            except Exception as e:
                print(e)
                already = True
            cursor.close()
            # cursor.execute("insert into emails (recepient_id, subject, body, created_at) values (%s, %s, %s, NOW())", [request.user.pk, "Booking Created", f"Your booking for seat {seat.name} has been created"])
            # cursor.execute("insert into sms(recepient_id, body, created_at) values (%s, %s, NOW())", [request.user.pk, f"Your booking for seat {seat.name} has been created)"])
        flight = Flight.objects.raw(f"select * from flights where flight_id = {request.POST.get('flight_id')}")[0]
    else:
        flight = Flight.objects.raw(f"select * from flights where flight_id = {request.GET.get('flight_id')}")[0]
    if request.method == "GET" and request.GET.get("available"):
        available = True
        seats = Seat.objects.raw(f"select * from seats where flight_id = {flight.pk} and seat_id not in (select seat_id from bookings where status != 'Cancelled')")
    else:
        seats = Seat.objects.raw(f"select * from seats where flight_id = {flight.pk}")
    cursor = connection.cursor()
    cursor.execute(f"select count(*) from seats where flight_id = {flight.pk} and seat_type='Economy' and seat_id not in (select seat_id from bookings where status != 'Cancelled')")
    economy_c = cursor.fetchone()[0]
    if not economy_c:
        economy_c = 0
    cursor.execute(f"select count(*) from seats where flight_id = {flight.pk} and seat_type='Business' and seat_id not in (select seat_id from bookings where status != 'Cancelled')")
    business_c = cursor.fetchone()[0]
    if not business_c:
        business_c = 0
    return render(request, "seatlist.html", context={"data":get_seat_data(seats, request), "flight_id":flight.pk, "already":already, "booking_id":0, "economy_c":economy_c, "business_c":business_c, "available":available})


# def BookSeatView(request):
#     if not request.user:
#         return redirect("login")
#     already=False
#     if request.method=="POST":
#         seat = Seat.objects.raw(f"select * from seat where id = {request.POST.get('seat_id')}")[0]
#         if Booking.objects.filter(seat=seat).exclude(status="Completed").exclude(status="Cancelled").exists():
#             already=True
#             booking = Booking.objects.get(seat=seat)
#         booking = Booking.objects.create(seat=seat, user=request.user, status="Pending")
#     else:
#         seat = Seat.objects.get(id=request.GET.get('seat_id'))
#     return render(request, "booked.html", context={"data":booking.id, "already":already})

def BookingListView(request):
    if not request.user.is_authenticated:
        return redirect("login")
    bookings = Booking.objects.raw(f"select * from bookings where user_id = '{request.user.pk}' and not status='Cancelled'")
    cursor = connection.cursor()
    cursor.execute(f"select sum(cost) from seats inner join price on price.seat_type=seats.seat_type and price.flight_id=seats.flight_id where seat_id in (select seat_id from bookings where user_id='{request.user.pk}' and (status='Confirmed' or status='Completed'));")    
    expense = cursor.fetchone()[0]
    if expense is None:
        expense = 0
    return render(request, "bookinglist.html", context={"data":get_booking_data(bookings), "expense":int(expense)})

def CancelBookingView(request):
    if not request.user.is_authenticated:
        return redirect("login")
    Booking.objects.raw(f"update bookings set status = 'Cancelled' where booking_id = {request.GET.get('booking_id')}")
    return render(request, "cancelled.html")

def CancellationListView(request):
    if not request.user.is_authenticated:
        return redirect("login")
    cancellations = Cancellation.objects.raw(f"select * from cancellations where booking_id in (select booking_id from bookings where user_id = '{request.user.pk}' and status = 'Cancelled')")
    return render(request, "cancellations.html", context={"data":get_cancellation_data(cancellations)})

def EmailListView(request):
    if not request.user.is_authenticated:
        return redirect("login")
    emails = Email.objects.raw(f"select * from emails where recepient_id = '{request.user.pk}' order by created_at desc")
    return render(request, "emails.html", context={"data":get_email_data(emails)})

def SmsListView(request):
    if not request.user.is_authenticated:
        return redirect("login")
    sms = SMS.objects.raw(f"select * from sms where recepient_id = '{request.user.pk}' order by created_at desc")
    return render(request, "sms.html", context={"data":get_sms_data(sms)})

# def GetBookingView(request):
#     booking = Booking.objects.get(id=request.GET.get('booking_id'))
#     return render(request, "booking.html", context={"data":get_booking_data([booking])})

def GetBookingView(request):
    if not request.user.is_authenticated:
        return redirect("login")
    cursor = connection.cursor()
    if not request.user:
        return redirect("login")
    if request.method=="POST" and request.POST.get('status') == "confirm":
        cursor.execute(f"update bookings set status = 'Confirmed' where booking_id = {request.POST.get('booking_id')}")
        booking = Booking.objects.raw(f"select * from bookings where booking_id = {request.POST.get('booking_id')}")[0]
        send_mail(subject="Booking Confirmed", message=f"Your booking for seat {booking.seat.name} has been confirmed", from_email=settings.EMAIL_HOST_USER, recipient_list=[request.user.email], fail_silently=True)
        cursor.execute("insert into emails (recepient_id, subject, body, created_at) values (%s, %s, %s, NOW())", [request.user.pk, "Booking Confirmed", f"Your booking for seat {booking.seat.name} has been confirmed"])
        cursor.execute("insert into sms(recepient_id, body, created_at) values (%s, %s, NOW())", [request.user.pk, f"Your booking for seat {booking.seat.name} has been confirmed"])
    elif request.method=="POST" and request.POST.get('status') == "cancel":
        cursor.execute(f"update bookings set status = 'Cancelled' where booking_id = {request.POST.get('booking_id')}")
        cursor.execute(f"insert into cancellations (booking_id, reason, created_at) values ({request.POST.get('booking_id')}, '{request.POST.get('cancel_reason')}', NOW())")
        booking = Booking.objects.raw(f"select * from bookings where booking_id = {request.POST.get('booking_id')}")[0]
        send_mail(subject="Booking Cancelled", message=f"Your booking for seat {booking.seat.name} has been cancelled", from_email=settings.EMAIL_HOST_USER, recipient_list=[request.user.email], fail_silently=True)
        cursor.execute("insert into emails (recepient_id, subject, body, created_at) values (%s, %s, %s, NOW())", [request.user.pk, "Booking Cancelled", f"Your booking for seat {booking.seat.name} has been cancelled"])
        cursor.execute("insert into sms(recepient_id, body, created_at) values (%s, %s, NOW())", [request.user.pk, f"Your booking for seat {booking.seat.name} has been cancelled"])
    else:
        booking = Booking.objects.raw(f"select * from bookings where booking_id = {request.GET.get('booking_id')}")[0]       
    return render(request, "booking.html", context={"booking":get_single_booking_data(booking)})