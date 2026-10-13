from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import random

from .forms import RegisterForm, ProfileForm
from .models import Profile


def login_view(request):
    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)

            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect("/")

        except User.DoesNotExist:
            pass

    return render(request, "login.html")


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            # OTP verified आहे का ते check करा
            if not request.session.get("email_otp_verified"):
                messages.error(
                    request,
                    "Please verify your email OTP first."
                )
                return render(
                    request,
                    "register.html",
                    {"form": form}
                )

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                first_name=form.cleaned_data["first_name"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            Profile.objects.create(
                user=user,
                phone=form.cleaned_data["phone"]
            )

            # OTP session clear
            request.session.pop("email_otp", None)
            request.session.pop("email_otp_verified", None)
            request.session.pop("otp_email", None)

            messages.success(
                request,
                "Account created successfully. Please login."
            )

            return redirect("login")

    else:
        form = RegisterForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )


def send_email_otp(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip()

        if not email:
            return JsonResponse({
                "success": False,
                "message": "Please enter your email."
            })

        # Check email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                "success": False,
                "message": "This email is already registered."
            })

        otp = str(random.randint(100000, 999999))

        request.session["email_otp"] = otp
        request.session["otp_email"] = email
        request.session["email_otp_verified"] = False

        try:

            send_mail(
                subject="HouseRent Email Verification OTP",
                message=(
                    f"Your HouseRent verification OTP is: {otp}\n\n"
                    "This OTP is valid for this registration session."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return JsonResponse({
                "success": True,
                "message": "OTP sent successfully."
            })

        except Exception as e:

            print("EMAIL OTP ERROR:", e)

            return JsonResponse({
                "success": False,
                "message": "OTP could not be sent. Check Gmail SMTP settings."
            })

    return JsonResponse({
        "success": False,
        "message": "Invalid request."
    })


def verify_email_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get("otp", "").strip()

        saved_otp = request.session.get("email_otp")

        if saved_otp and entered_otp == saved_otp:

            request.session["email_otp_verified"] = True

            return JsonResponse({
                "success": True,
                "message": "Email verified successfully."
            })

        return JsonResponse({
            "success": False,
            "message": "Invalid OTP."
        })

    return JsonResponse({
        "success": False,
        "message": "Invalid request."
    })


def logout_view(request):
    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("/")


@login_required(login_url="login")
def profile_view(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile Updated Successfully."
            )

            return redirect("profile")

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        "profile.html",
        {
            "profile": profile,
            "form": form,
        }
    )
    
    from django.contrib.auth.models import User
from properties.models import Property
from bookings.models import Booking


@login_required(login_url="login")
def admin_dashboard(request):

    # Only admin/staff users
    if not request.user.is_staff:
        return redirect("/")

    total_users = User.objects.count()
    total_properties = Property.objects.count()
    total_bookings = Booking.objects.count()

    pending_bookings = Booking.objects.filter(
        status="Pending"
    ).count()

    approved_bookings = Booking.objects.filter(
        status="Approved"
    ).count()

    rejected_bookings = Booking.objects.filter(
        status="Rejected"
    ).count()

    recent_bookings = Booking.objects.select_related(
        "property",
        "user"
    ).order_by("-booking_date")[:10]

    return render(
        request,
        "admin_dashboard.html",
        {
            "total_users": total_users,
            "total_properties": total_properties,
            "total_bookings": total_bookings,
            "pending_bookings": pending_bookings,
            "approved_bookings": approved_bookings,
            "rejected_bookings": rejected_bookings,
            "recent_bookings": recent_bookings,
        }
    )