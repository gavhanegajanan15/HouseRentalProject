from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from properties.models import Property
from .models import Wishlist


@login_required(login_url="login")
def add_to_wishlist(request, property_id):

    property = get_object_or_404(Property, id=property_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        property=property
    )

    return redirect("property_detail", id=property_id)


@login_required(login_url="login")
def my_wishlist(request):

    wishlist = Wishlist.objects.filter(
        user=request.user
    ).order_by("-added_at")

    return render(request, "my_wishlist.html", {
        "wishlist": wishlist
    })


@login_required(login_url="login")
def remove_from_wishlist(request, id):

    item = get_object_or_404(
        Wishlist,
        id=id,
        user=request.user
    )

    item.delete()

    return redirect("my_wishlist")