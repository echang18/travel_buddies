from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.regValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create(name=request.POST["name"], username=request.POST["username"], password=hashed_pw.decode())

        request.session['id'] = new_user.id
        return redirect('/travels')
        
def login(request):
    errors = User.objects.loginValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/')
    else:
        user_list = User.objects.filter(username=request.POST['username'])
        user = user_list[0]
        request.session['id'] = user.id
        return redirect('/travels')

def travels(request):
    if 'id' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id=request.session["id"])
        all_trips = Trip.objects.all()
        my_trips = user.trips.all()
        other_trips = all_trips.difference(my_trips)
        context = {
            'user' : user,
            'my_trips' : my_trips,
            'other_trips' : other_trips,
        }
        return render(request, "dashboard.html", context)

def add(request):
    if 'id' not in request.session:
        return redirect("/")
    else:
        return render(request, "add_trip.html")

def create(request):
    errors = Trip.objects.tripValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add')
    else:
        user = User.objects.get(id=request.session["id"])
        trip = Trip.objects.create(destination=request.POST["destination"], description=request.POST["description"], travel_date_from=request.POST['travel_date_from'], travel_date_to=request.POST['travel_date_to'], added_by_id=request.session['id'])
        user.trips.add(trip)
        return redirect('/travels')

def destination(request, id):
    if 'id' not in request.session:
        return redirect("/")
    else:
        some_trip = Trip.objects.get(id=id)
        users = some_trip.users.all()
        context = {
            "trip" : some_trip,
            "users" : users
        }
        return render(request, "show_trip.html", context)

def join(request, trip_id):
    user = User.objects.get(id=request.session["id"])
    trip = Trip.objects.get(id=trip_id)
    user.trips.add(trip)
    return redirect("/travels")

def logout(request):
    request.session.clear()
    return redirect("/")