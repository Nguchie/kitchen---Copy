from django.db import models


# ----------------------
# Abstract Base Property
# ----------------------
class PropertyBase(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_on_application = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def display_price(self):
        return "On Application" if self.price_on_application else f"${self.price:,.2f}"

    def __str__(self):
        return self.name


# -------------------
# BUY CATEGORY
# -------------------

class BuyDevelopment(PropertyBase):
    beds = models.IntegerField()
    floorplans = models.FileField(upload_to='floorplans/', null=True, blank=True)


class CommercialBuy(PropertyBase):
    size = models.CharField(max_length=100)
    description = models.TextField(blank=True)


class BuyLand(PropertyBase):
    size = models.CharField(max_length=100)
    description = models.TextField(blank=True)


# -------------------
# RENT CATEGORY
# -------------------

class ResidentialRent(PropertyBase):
    PROPERTY_TYPES = [
        ('unfurnished', 'Unfurnished'),
        ('furnished', 'Furnished'),
        # Add more types as needed
    ]
    type = models.CharField(max_length=50, choices=PROPERTY_TYPES)

    # Amenities as separate model with images (below)


class CommercialRent(PropertyBase):
    size = models.CharField(max_length=100)
    description = models.TextField(blank=True)


# -------------------
# IMAGES FOR LISTINGS
# -------------------

class PropertyImage(models.Model):
    image = models.ImageField(upload_to='property_images/')
    caption = models.CharField(max_length=255, blank=True)

    development = models.ForeignKey('Development', null=True, blank=True, on_delete=models.CASCADE, related_name='images')
    commercial_buy = models.ForeignKey('CommercialBuy', null=True, blank=True, on_delete=models.CASCADE, related_name='images')
    land = models.ForeignKey('Land', null=True, blank=True, on_delete=models.CASCADE, related_name='images')
    residential_rent = models.ForeignKey('ResidentialRent', null=True, blank=True, on_delete=models.CASCADE, related_name='images')
    commercial_rent = models.ForeignKey('CommercialRent', null=True, blank=True, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.caption or f"Image {self.id}"


# -------------------
# AMENITIES (FOR RESIDENTIAL RENT)
# -------------------

class ResidentialAmenity(models.Model):
    property = models.ForeignKey('ResidentialRent', on_delete=models.CASCADE, related_name='amenities')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='amenities/')

    def __str__(self):
        return self.name
