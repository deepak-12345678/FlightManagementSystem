from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Flight)
admin.site.register(Seat)
admin.site.register(Booking)
admin.site.register(Cancellation)
admin.site.register(Email)
admin.site.register(SMS)

