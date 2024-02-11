from django.contrib.gis.db import models as gis_models
from django.db import models
from django.conf import settings
from common.custom_exceptions import HttpException
from listings.constants import PROPERTY_TYPE_CHOICES, PROPERTY_LABEL_CHOICES

class Location(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    pin_code = models.CharField(max_length=10, default="")
    lat = gis_models.FloatField(null=True, blank=True)
    lng = gis_models.FloatField(null=True, blank=True)
    address = models.TextField(default="")

    def save(self, *args, **kwargs):
        super(Location, self).save(*args, **kwargs)

class City(models.Model):
    name = models.SlugField(max_length=50, null=True, blank=True, db_index=True)
    display_name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    lat = gis_models.FloatField(null=True, blank=True)
    lng = gis_models.FloatField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(City, self).save(*args, **kwargs)

class Property(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=30, decimal_places=2, default=0.0)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    sold = models.BooleanField(default=False)
    area = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='apartment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        result = super(Property, self).save(*args, **kwargs)
        return result

class PropertyFiles(models.Model):
    property = models.ForeignKey(Property, related_name='urls', on_delete=models.CASCADE)
    url = models.CharField(max_length=500)
    label = models.CharField(max_length=20, choices=PROPERTY_LABEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(PropertyFiles, self).save(*args, **kwargs)