from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
	path('travels', views.travels),
    path('add', views.add),
    path('create', views.create),
    path('travels/destination/<id>', views.destination),
    path('join/<trip_id>', views.join),
    path('logout', views.logout),
]
