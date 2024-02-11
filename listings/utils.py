"""
This is a logic building layer (or, Aggregation layer), which we'll utilize to
make external/internal calls to database models, REST calls to ext. services and
aggregate the data.
"""

from listings.serializers import PropertyListingSerializer
from listings.interface.database_service import PropertyListingService
from listings.constants import RENT_PROPERTY_PRICES, NON_RENT_PROPERTY_PRICES

class PropertyListingUtil:

    @classmethod
    def get_properties_details(cls, **kwargs):
        property_id = kwargs.get("property_id")
        property_type = kwargs.get("property_type")
        min_price = kwargs.get("min_price")
        max_price = kwargs.get("max_price")
        location = kwargs.get("location")
        bedrooms = kwargs.get("bedrooms")
        bathrooms = kwargs.get("bathrooms")
        area = kwargs.get("area")

        if not all(min_price, max_price):
            if property_type == "house":
                min_price = min_price or RENT_PROPERTY_PRICES[0]
                max_price = max_price or RENT_PROPERTY_PRICES[-1]
            elif property_type == "apartment":
                min_price = min_price or NON_RENT_PROPERTY_PRICES[0]
                max_price = max_price or NON_RENT_PROPERTY_PRICES[-1]

        filter_dict = {
            **({"price__gte": min_price} if min_price else {}),
            **({"price__lte": max_price} if max_price else {}),
            **({"location": location} if location else {}),
            **({"bedrooms": bedrooms} if bedrooms else {}),
            **({"bathrooms": bathrooms} if bathrooms else {}),
            **({"area": area} if area else {}),
        }
        properties = PropertyListingService.get_property_queryset(filter_dict)
        if property_id:
            property = PropertyListingService.get_property(property_id=property_id)
            data = PropertyListingSerializer(property).data
            return data
        properties_data = PropertyListingSerializer(properties, many=True).data
        return properties_data
    
    @classmethod
    def add_property_details(cls, payload):
        # Upload the binary(propety images/documents) to s3 bucket and add the links in DB.
        # Rest details can be directly added to db
        ...