from django.urls import path
from . import views

urlpatterns = [

    path(
        "wishlist/add/<int:property_id>/",
        views.add_to_wishlist,
        name="add_to_wishlist"
    ),

    path(
        "my-wishlist/",
        views.my_wishlist,
        name="my_wishlist"
    ),

    path(
        "wishlist/remove/<int:id>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist"
    ),

]