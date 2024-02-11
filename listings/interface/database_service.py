from listings.models import Property, City, Location, PropertyFiles
from django.contrib.auth import get_user_model


class PropertyListingService:
    
    @classmethod
    def get_property_queryset(cls, filters_dict, exclude_filter_dict):
        filters_dict = {filter_key: filter_val for filter_key, filter_val in filters_dict.items()
                        if all(filter_key, filter_val)}

        exclude_filter_dict = {ex_filter_key: ex_filter_val
                               for ex_filter_key, ex_filter_val in exclude_filter_dict.items()
                               if all(ex_filter_key, ex_filter_val)}

        property_obj = Property.objects.filter(**filters_dict).exclude(
            **exclude_filter_dict)
        return property_obj

    @classmethod
    def get_property(cls, property_id):
        if not property_id:
            return None
        property_qs = cls.get_property_queryset({"id": property_id})
        return property_qs and property_qs.first()

    @classmethod
    def create_property(cls, **kwargs):
        user = get_user_model()
        owner = user.objects.filter(id=kwargs.get("user_id"))
        if not owner:
            raise Exception("User not found")

        city = City.objects.filter(name=kwargs.get("city_name"), is_active=True)

        if not city:
            location = Location(pin_code=kwargs.get("pin_code"),
                                address=kwargs.get("address"))
            location.save()
            city = City(name=kwargs.get("city_name"),
                        display_name=kwargs.get("city_display_name"),
                        is_active=True,
                        lat=kwargs.pop("city_lat", None),
                        lng=kwargs.pop("city_lng", None),
                        location=location)
            city.save()

        property = Property(
            title=kwargs.get("property_title"),
            description=kwargs.get("property_description"),
            price=kwargs.get("property_price"),
            city=city,
            bedrooms=kwargs.get("property_bedrooms"),
            bathrooms=kwargs.get("property_bathrooms"),
            area=kwargs.get("property_area"),
            owner=user,
            property_type=kwargs.get("property_type")
        )

        property.save()
        return property and property.id
    
    @classmethod
    def update_property(cls, **kwargs):
        if kwargs.get("property_id") is None:
            raise Exception("property_id is a mandatory field to update property details")
        
        property = cls.get_property(kwargs.get("property_id"))
        
        if not property:
            raise Exception("Property with id: {} does not exist")
        
        existing_property_data = property.__dict__
        
        changed_fields_data = {
            key: kwargs[key]
            for key in existing_property_data
            if key in kwargs and kwargs[key] != existing_property_data[key]
        }

        for _key, _val in changed_fields_data.items():
            setattr(property, _key, _val)

        property.save()
        return True