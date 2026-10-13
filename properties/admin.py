from django.contrib import admin
from .models import Property, ContactMessage


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "property_type",
        "location",
        "price",
        "bedrooms",
        "is_available",
    )

    list_filter = (
        "property_type",
        "location",
        "is_available",
    )

    search_fields = (
        "title",
        "location",
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "subject",
        "created_at",
    )

    search_fields = (
        "full_name",
        "email",
        "subject",
    )

    list_filter = (
        "created_at",
    )