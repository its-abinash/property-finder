from django.contrib.gis.db import models as gis_models
from django.db import models
from django.conf import settings
from listings.constants import PROPERTY_TYPE_CHOICES, PROPERTY_LABEL_CHOICES

class Location(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    pin_code = models.CharField(max_length=10, default="")
    address = models.TextField()

    def save(self, *args, **kwargs):
        super(Location, self).save(*args, **kwargs)
    
    class Meta:
        managed = False

class City(models.Model):
    name = models.SlugField(max_length=50, null=True, blank=True, db_index=True)
    display_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    lat = gis_models.FloatField(null=True, blank=True)
    lng = gis_models.FloatField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(City, self).save(*args, **kwargs)
    
    class Meta:
        managed = False

class Property(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Property, self).save(*args, **kwargs)
    
    class Meta:
        managed = False

class PropertyFiles(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.CharField(max_length=500)
    label = models.CharField(max_length=20, choices=PROPERTY_LABEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(PropertyFiles, self).save(*args, **kwargs)
    
    class Meta:
        managed = False