from django.urls import path
from . import views

urlpatterns = [
    path('booking/', views.booking_form, name='booking_form'),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("cancel-booking/<int:id>/", views.cancel_booking, name="cancel_booking"),
]