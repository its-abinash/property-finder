from rest_framework import serializers
from listings.models import Property
from listings.interface.database_service import PropertyListingService

class PropertyListingSerializer(serializers.ModelSerializer):
    city_details = serializers.SerializerMethodField()
    property_details = serializers.SerializerMethodField()
    owner_details = serializers.SerializerMethodField()
    created_at = serializers.CharField()
    updated_at = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super(PropertyListingSerializer, self).__init__(*args, **kwargs)
    
    def get_city_details(self, property_obj):
        city = getattr(property_obj, "city", None)
        return {
            "city": getattr(city, "name", None),
            "lat": getattr(city, "lat", None),
            "long": getattr(city, "lng", None)
        }

    def get_property_details(self, property_obj):
        city = getattr(property_obj, "city", None)
        location = getattr(city, "location", None)
        property_document = PropertyListingService.get_property_documents(
            property_obj.id)
        return {
            "name": getattr(property_obj, "title", None),
            "description": getattr(property_obj, "description", None),
            "price": getattr(property_obj, "price", None),
            "bedrooms": getattr(property_obj, "bedrooms", None),
            "bathrooms": getattr(property_obj, "bathrooms", None),
            "total_area": getattr(property_obj, "area", None),
            "property_type": getattr(property_obj, "property_type", None),
            "lat": getattr(location, "lat", None),
            "long": getattr(location, "lng", None),
            "sold": getattr(property_obj, "sold", False),
            "documents": property_document
        }

    def get_owner_details(self, property_obj):
        owner = getattr(property_obj, "owner", None)
        return {
            "name": getattr(owner, "full_name", None),
            "contact_number": getattr(owner, "contact_number", None),
        }

    class Meta:
        model = Property
        fields = ['city_details', 'property_details', 'owner_details',
                  'created_at', 'updated_at']
