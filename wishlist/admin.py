from django.contrib import admin
from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "property",
        "added_at",
    )

    search_fields = (
        "user__username",
        "property__title",
    )

    list_filter = (
        "added_at",
    )