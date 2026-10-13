from django.db import models


class Property(models.Model):

    PROPERTY_TYPES = [
        ("Apartment", "Apartment"),
        ("House", "House"),
        ("Villa", "Villa"),
    ]

    title = models.CharField(max_length=200)

    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES
    )

    location = models.CharField(max_length=200)

    price = models.IntegerField()

    bedrooms = models.IntegerField()

    bathrooms = models.IntegerField()

    area = models.IntegerField(
        help_text="Square Feet"
    )

    image = models.ImageField(
        upload_to="properties/"
    )

    description = models.TextField()

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return self.title


class ContactMessage(models.Model):

    full_name = models.CharField(max_length=100)

    email = models.EmailField()

    subject = models.CharField(max_length=200)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject}"
    