from listings.models import Property, City, Location, PropertyFiles
from django.contrib.auth import get_user_model
from common.custom_exceptions import HttpException
from listings.constants import ALLOWED_PROPERTY_FILEDS_TO_UPDATE


class PropertyListingService:

    @classmethod
    def get_property_queryset(cls, filters_dict=None, exclude_filter_dict=None):
        filters_dict = filters_dict or {}
        exclude_filter_dict = exclude_filter_dict or {}
        filters_dict = {filter_key: filter_val for filter_key, filter_val in filters_dict.items()
                        if all((filter_key, filter_val))}

        exclude_filter_dict = {ex_filter_key: ex_filter_val
                               for ex_filter_key, ex_filter_val in exclude_filter_dict.items()
                               if all((ex_filter_key, ex_filter_val))}

        property_obj = Property.objects.filter(**filters_dict).exclude(
            **exclude_filter_dict)
        return property_obj
    
    @classmethod
    def get_city(cls, city_name):
        city = City.objects.filter(name=city_name, is_active=True)
        return city and city.first()

    @classmethod
    def get_property(cls, property_id):
        if not property_id:
            return None
        property_qs = cls.get_property_queryset({"id": property_id})
        return property_qs and property_qs.first()

    @classmethod
    def get_location(cls, pincode, lat, lng):
        location = Location.objects.filter(pin_code=pincode, lat=lat, lng=lng).first()
        return location

    @classmethod
    def add_location(cls, pincode, lat, lng, address):
        location = Location(pin_code=pincode, address=address, lat=lat, lng=lng)
        location.save()
        return location
    
    @classmethod
    def add_city(cls, city_info, location):
        city = City(name=city_info.get("name"),
                    display_name=city_info.get("display_name"),
                    is_active=True,
                    lat=city_info.get("lat", None),
                    lng=city_info.get("lng", None),
                    location=location)
        city.save()
        return city
    
    @classmethod
    def add_property_documents(cls, property, property_documents):
        property_docs_to_create = [
            PropertyFiles(property=property,
                          url=property_doc.get("url"),
                          label=property_doc.get("label"))
            for property_doc in property_documents
        ]
        PropertyFiles.objects.bulk_create(property_docs_to_create)
    
    @classmethod
    def get_property_documents(cls, property_id):
        result = []
        property_docs = PropertyFiles.objects.filter(property_id=property_id)
        for doc in property_docs:
            url = getattr(doc, "url", None)
            result.append({
                "url": url,
                "label": getattr(doc, "label", None),
                "slug": url and url.split("/")[-2] # hex slug of s3 bucket object
            })
        return result

    @classmethod
    def create_property(cls, owner_id, owner_user_name, owner_contact_number, **kwargs):
        user = get_user_model()
        owner = None
        if owner_user_name:
            owner = user.objects.filter(user_name=owner_user_name).last()
        elif owner_id:
            owner = user.objects.filter(id=owner_id).last()
        elif owner_contact_number:
            owner = user.objects.filter(contact_number=owner_contact_number).last()
        if not owner:
            raise HttpException(error="Owner not found with given details",
                                status_code=401)

        location_info = kwargs.get("location_info") or {}
        property_info = kwargs.get("property_info") or {}
        city_info = kwargs.get("city_info") or {}
        property_docs = kwargs.get("uploaded_docs") or []

        city = cls.get_city(city_info.get("name"))

        if not city:
            pincode = location_info.get("pincode")
            lat = location_info.get("lat")
            lng = location_info.get("lng")
            address = location_info.get("address")
            location = cls.get_location(pincode, lat, lng)
            if not location:
                location = cls.add_location(pincode, lat, lng, address)
            city = cls.add_city(city_info, location)

        property = Property(
            title=property_info.get("title"),
            description=property_info.get("description"),
            price=property_info.get("price"),
            city=city,
            bedrooms=property_info.get("bedrooms"),
            bathrooms=property_info.get("bathrooms"),
            area=property_info.get("area"),
            owner=owner,
            property_type=property_info.get("type")
        )

        property.save()

        if property_docs:
            cls.add_property_documents(property, property_docs)

        return property and property.id

    @classmethod
    def update_property(cls, property_id, uploaded_docs, payload):
        property = cls.get_property(property_id)
        property_documents = uploaded_docs or []
        if payload.get("sold"):
            is_sold = True if str(payload.get("sold", "false")).lower() == 'true' else False
            payload['sold'] = is_sold

        if not property:
            raise HttpException(error="Property with id: {} does not exist".format(
                property_id), status_code=400)
        
        if property_documents:
            PropertyListingService.add_property_documents(property, property_documents)

        existing_property_data = property.__dict__
        
        changed_fields_data = {
            key: payload[key]
            for key in existing_property_data
            if key in payload.keys() and payload[key] != existing_property_data[key] and \
            key in ALLOWED_PROPERTY_FILEDS_TO_UPDATE
        }

        setattr(property, "pk", property_id)

        for _key, _val in changed_fields_data.items():
            setattr(property, _key, _val)

        property.save()
        return property and property.id