from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "email",
        "phone",
        "property",
        "visit_date",
        "status",
        "booking_date",
    )

    list_filter = (
        "status",
        "visit_date",
        "booking_date",
    )

    search_fields = (
        "full_name",
        "email",
        "phone",
        "property__title",
        "property__location",
    )

    list_editable = (
        "status",
    )

    ordering = (
        "-booking_date",
    )


    def save_model(self, request, obj, form, change):

        old_status = None

        if change:
            try:
                old_booking = Booking.objects.get(
                    pk=obj.pk
                )
                old_status = old_booking.status
            except Booking.DoesNotExist:
                pass


        super().save_model(
            request,
            obj,
            form,
            change
        )


        # Status changed
        if change and old_status != obj.status:

            # -------------------------------
            # APPROVED EMAIL
            # -------------------------------

            if obj.status == "Approved":

                send_mail(
                    subject="HouseRent - Booking Approved",

                    message=f"""
Hello {obj.full_name},

Good news! 🎉

Your HouseRent property booking has been APPROVED.

Booking Details
------------------------------

Property: {obj.property.title}
Location: {obj.property.location}
Visit Date: {obj.visit_date}

Booking Status: APPROVED

Please visit the property on your scheduled visit date.

Thank you for choosing HouseRent.

Regards,
HouseRent Team
""",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[
                        obj.email
                    ],

                    fail_silently=False,
                )


            # -------------------------------
            # REJECTED EMAIL
            # -------------------------------

            elif obj.status == "Rejected":

                send_mail(
                    subject="HouseRent - Booking Update",

                    message=f"""
Hello {obj.full_name},

We are sorry to inform you that your HouseRent property booking has been REJECTED.

Booking Details
------------------------------

Property: {obj.property.title}
Location: {obj.property.location}
Visit Date: {obj.visit_date}

Booking Status: REJECTED

You can explore other available properties on HouseRent.

Thank you for using HouseRent.

Regards,
HouseRent Team
""",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[
                        obj.email
                    ],

                    fail_silently=False,
                )