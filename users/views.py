from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.db import connection
# Create your views here.
User = get_user_model()
def login(request):
    logout(request)
    return render(request, "login.html")


def reqistration(request):
    if request.method == "POST":
        email = request.POST["email"]
        name = request.POST["name"]
        password = request.POST["password"]
        dob = request.POST["date"]
        cursor = connection.cursor()
        cursor.execute("INSERT INTO passengers (email, name, password, date_of_birth) VALUES (%s, %s, %s, %s)", [email, name, password, dob])
        return redirect("login")
    return render(request, "registration.html")