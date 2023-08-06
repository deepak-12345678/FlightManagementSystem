from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import connection

class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have an password address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        # extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('is_staff', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user




class Passenger(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('NB','Non-Binary')
    )
    username=None
    is_superuser=None
    is_staff=None
    is_active=None
    gender = None
    first_name = None
    last_name = None
    date_joined = None
    last_login = None
    password = models.CharField(max_length=100)
    email = models.EmailField(_('email address'), primary_key=True)
    date_of_birth = models.DateField(blank=True,null=True)
    name = models.CharField(max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = "passengers"
# Create your models here.
BOOKING_STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Confirmed", "Confirmed"), 
    ("Cancelled", "Cancelled"),
    ("Completed", "Completed")
]
from django.contrib.auth import get_user_model
UserC = get_user_model()

class Flight(models.Model):
    flight_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)


    def __str__(self) -> str:
        return self.name +" " + self.source + "---" + self.destination
    
    class Meta:
        db_table = "flights"

SEAT_TYPE_CHOICES = [
    ("Economy", "Economy"),
    ("Business", "Business"),
]


class Seat(models.Model):
    seat_id = models.AutoField(primary_key=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="seats")
    seat_type = models.CharField(max_length=100, choices=SEAT_TYPE_CHOICES)


    class Meta:
        db_table = "seats"

    @property
    def name(seat):
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM seats WHERE flight_id = %s AND seat_type = %s", [seat.flight.flight_id, seat.seat_type])
        n = cursor.fetchone()[0]
        return seat.seat_type + " " + str((seat.seat_id-1)%n+1)



class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="bookings")
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES)
    user = models.ForeignKey(UserC, related_name="Bookings", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # unique_together = ["seat", "user"]
        db_table = "bookings"



class Cancellation(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="cancellation", primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()

    class Meta:
        db_table = "cancellations"


class Email(models.Model):
    em_id = models.AutoField(primary_key=True)
    recipient = models.ForeignKey(UserC, on_delete=models.CASCADE, related_name="emails")
    subject = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "emails"


class SMS(models.Model):
    sms_id = models.AutoField(primary_key=True)
    recipient = models.ForeignKey(UserC, on_delete=models.CASCADE, related_name="sms")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sms"