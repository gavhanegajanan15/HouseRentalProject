from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Booking
from properties.models import Property


@login_required(login_url='login')
def booking_form(request):

    property_id = request.GET.get("property")

    property = None

    if property_id:
        property = get_object_or_404(Property, id=property_id)

    if request.method == "POST":

        # Booking data
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        visit_date = request.POST.get("visit_date")
        message = request.POST.get("message")

        # Save booking
        booking = Booking.objects.create(
            user=request.user,
            property=property,
            full_name=full_name,
            email=email,
            phone=phone,
            visit_date=visit_date,
            message=message,
        )

        property_title = (
            property.title if property else "Property"
        )

        property_location = (
            property.location if property else "Not Available"
        )

        # ------------------------------------------------
        # 1. CUSTOMER BOOKING CONFIRMATION EMAIL
        # ------------------------------------------------

        customer_email = email or request.user.email

        if customer_email:

            send_mail(
                subject="HouseRent - Booking Confirmation",

                message=f"""
Hello {full_name or request.user.first_name or request.user.username},

Your property booking request has been received successfully.

Booking Details
------------------------------

Property: {property_title}
Location: {property_location}
Visit Date: {visit_date}

Name: {full_name}
Email: {customer_email}
Phone: {phone}

Message:
{message or "No message provided"}

Thank you for choosing HouseRent.

Regards,
HouseRent Team
""",

                from_email=settings.DEFAULT_FROM_EMAIL,

                recipient_list=[
                    customer_email
                ],

                fail_silently=False,
            )


        # ------------------------------------------------
        # 2. ADMIN BOOKING NOTIFICATION EMAIL
        # ------------------------------------------------

        admin_email = "houserentportal2026@gmail.com"

        send_mail(
            subject="HouseRent - New Booking Received",

            message=f"""
Hello Admin,

A new property booking has been received.

Booking Details
------------------------------

Property: {property_title}
Location: {property_location}
Visit Date: {visit_date}

Customer Name: {full_name}
Customer Email: {customer_email}
Customer Phone: {phone}

Customer Message:
{message or "No message provided"}

Booking Status:
Pending

Please login to the HouseRent Admin Panel
to review this booking.

Regards,
HouseRent System
""",

            from_email=settings.DEFAULT_FROM_EMAIL,

            recipient_list=[
                admin_email
            ],

            fail_silently=False,
        )


        messages.success(
            request,
            "Booking Successful! Confirmation email sent successfully."
        )

        return redirect("/")


    return render(
        request,
        "booking_form.html",
        {
            "property": property
        }
    )


@login_required(login_url='login')
def my_bookings(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by("-booking_date")

    return render(
        request,
        "my_bookings.html",
        {
            "bookings": bookings
        }
    )


@login_required(login_url='login')
def cancel_booking(request, id):

    booking = get_object_or_404(
        Booking,
        id=id,
        user=request.user
    )

    if booking.status == "Pending":
        booking.delete()

    return redirect("my_bookings")