from django.db import models
from datetime import datetime, timedelta
import bcrypt

NOW = str(datetime.now())

class UserManager(models.Manager):
    def regValidator(self, form):
        errors = {}
        if not form['name']:
            errors['name'] = "Please enter a name."
        elif len(form['name']) < 3:
            errors['name'] = "name must be at least three characters long."

        if not form['username']:
            errors['username'] = "Please enter a username."
        elif len(form['username']) < 3:
            errors['username'] = "Username must be at least three characters long."
        elif User.objects.filter(username=form["username"]):
            errors['username'] = "Username already in database, please login."
        
        if not form['password']:
            errors['password'] = "Please enter a password."
        elif len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        
        if not form['confirm_password']:
            errors['confirm_password'] = "Please enter a confirm password."
        elif form['confirm_password'] != form['password']:
            errors['confirm_password'] = "Passwords must match."

        return errors
    
    def loginValidator(self, form):
        errors = {}

        if not form['username']:
            errors['username'] = "Please enter a username."
        elif not User.objects.filter(username=form["username"]):
            errors['username'] = "Username not found. Please register."
        else:
            user_list = User.objects.filter(username=form["username"])
            user = user_list[0]
            if not bcrypt.checkpw(form['password'].encode(), user.password.encode()):
                errors['password'] = "Wrong password."
            if not form['password']:
                errors['password'] = "Please enter a password."

        return errors

class TripManager(models.Manager):
    def tripValidator(self, form):
        errors = {}
        if not form['destination']:
            errors['destination'] = "Please enter a destination."
        elif len(form['destination']) == 0:
            errors['name'] = "Destination field must not be blank."

        if not form['description']:
            errors['description'] = "Please enter a description."
        elif len(form['description']) == 0:
            errors['name'] = "Description field must not be blank."

        if not form['travel_date_from']:
            errors['travel_date_from'] = "Please enter your departure date."
        elif form["travel_date_from"] < NOW:
            errors['travel_date_from'] = "Departure date must be in the future."

        if not form['travel_date_to']:
            errors['travel_date_to'] = "Please enter your returning date."
        elif form["travel_date_to"] < form["travel_date_from"]:
            errors['travel_date_to'] = "Returning date must be set after departure date." 

        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    travel_date_from = models.DateTimeField()
    travel_date_to = models.DateTimeField()
    users = models.ManyToManyField(User, related_name="trips")
    added_by = models.ForeignKey(User, related_name="trips_added", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
    def traveler(self):
        return self.users.exclude(id=self.added_by.id)