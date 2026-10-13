from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Property, ContactMessage


def index(request):

    properties = Property.objects.filter(is_available=True)

    # Search Filters
    location = request.GET.get('location')
    property_type = request.GET.get('property_type')
    price = request.GET.get('price')

    if location:
        properties = properties.filter(location__icontains=location)

    if property_type:
        properties = properties.filter(property_type=property_type)

    if price:
        properties = properties.filter(price__lte=price)

    properties = properties[:3]

    return render(request, "index.html", {
        "properties": properties
    })


def property_detail(request, id):

    property = get_object_or_404(Property, id=id)

    return render(request, "property_detail.html", {
        "property": property
    })


# All Properties Page
def property_list(request):

    properties = Property.objects.filter(is_available=True)

    return render(request, "property_list.html", {
        "properties": properties
    })

def about(request):
    return render(request, "about.html")

def contact(request):

    if request.method == "POST":

        ContactMessage.objects.create(

            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),

        )

        messages.success(
            request,
            "Your message has been sent successfully!"
        )

    return render(request, "contact.html")