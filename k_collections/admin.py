from django.contrib import admin
from .models import (
    Development, CommercialBuy, Land,
    ResidentialRent, CommercialRent,
    PropertyImage, ResidentialAmenity
)


# ---------------------
# Inlines for Images
# ---------------------

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


# ---------------------
# Inline for Amenities (ResidentialRent only)
# ---------------------

class AmenityInline(admin.TabularInline):
    model = ResidentialAmenity
    extra = 1


# ---------------------
# Admins for Each Property Type
# ---------------------

@admin.register(Development)
class DevelopmentAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('name', 'location', 'beds', 'display_price')


@admin.register(CommercialBuy)
class CommercialBuyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('name', 'location', 'size', 'display_price')


@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('name', 'location', 'size', 'display_price')


@admin.register(ResidentialRent)
class ResidentialRentAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline, AmenityInline]
    list_display = ('name', 'location', 'type', 'display_price')


@admin.register(CommercialRent)
class CommercialRentAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('name', 'location', 'size', 'display_price')


# ---------------------
# Hide Image/Amenity Direct Models from Admin (Optional)
# ---------------------

admin.site.unregister(PropertyImage) if admin.site.is_registered(PropertyImage) else None
admin.site.unregister(ResidentialAmenity) if admin.site.is_registered(ResidentialAmenity) else None
