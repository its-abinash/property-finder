"""
This is a logic building layer (or, Aggregation layer), which we'll utilize to
make external/internal calls to database models, REST calls to ext. services and
aggregate the data.
"""
import os
import json
import zipfile
import mimetypes
import shutil
import copy
from django.utils import timezone
from listings.serializers import PropertyListingSerializer
from common.aws.services import FileUploadService
from listings.interface.database_service import PropertyListingService
from common.custom_exceptions import HttpException
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

        if not all((min_price, max_price)):
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
        properties_data = list(properties_data)
        # sorting the properties data according to sold=False
        properties_data.sort(
            key=lambda data: data and data.get("property_details", {}).get("sold"))
        return {"data": properties_data}

    @classmethod
    def upload_property_documents_to_s3(cls, property_document_files):
        extract_dir = 'extracted_files'
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        os.makedirs(extract_dir, exist_ok=True)
        uploaded_file_name = getattr(property_document_files, 'name', "").split(".")
        uploaded_file_name = uploaded_file_name and uploaded_file_name[0]
        with zipfile.ZipFile(property_document_files, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        uploaded_files = []
        
        for foldername in os.listdir(extract_dir): # main directories of property documents
            if not foldername.startswith("__"): # excluding cache directories
                directory = os.path.join(extract_dir, foldername)
                if os.path.exists(directory) and os.listdir(directory):
                    for root, dirs, files in os.walk(directory): # Traversing the root folder to access files
                        for file in files:
                            if file.startswith("."): # excluding cache files
                                continue
                            file_path = os.path.join(root, file)
                            uploaded_files.append(file_path) # saving main files in list
        uploaded_documents = []
        for _dir in uploaded_files:
            with open(_dir, 'rb') as _file:
                mimetype, _ = mimetypes.guess_type(_dir)
                filename = _dir.split('/')[-1]
                if not filename:
                    continue
                uploaded_file_url = FileUploadService.upload_media_file(
                    file=_file, content_type=mimetype, file_name=filename)
                if uploaded_file_url:
                    label = filename.split(".")[0] # bedroom.jpeg --> label = bedroom
                    uploaded_documents.append({
                        "url": uploaded_file_url,
                        "label": str(label).lower(),
                    })
        
        # removing the temp files that was holding the property docs
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        
        return uploaded_documents

    @classmethod
    def add_property_details(cls, payload, property_documents):
        # Upload the binary(propety images/documents) to s3 bucket and add the links in DB.
        # Rest details can be directly added to db
        # Accessing the request payload as formdata, since we're giving access to the property owner
        # to upload documents/images of property 

        owner_info = json.loads(payload.get("owner_info"))
        location_info = json.loads(payload.get("location_info"))
        property_info = json.loads(payload.get("property_info"))

        owner_id = owner_info.get("id")
        owner_user_name = owner_info.get("username")
        owner_contact_number = owner_info.get("contact_number")
        city_info = location_info.pop("city_info", None)

        if not any((owner_id, owner_user_name, owner_contact_number)):
            raise HttpException(error="owner details required to create property details",
                                status_code=400)

        uploaded_docs = cls.upload_property_documents_to_s3(property_documents)

        property_id = PropertyListingService.create_property(
            owner_id, owner_user_name, owner_contact_number,
            location_info=location_info, property_info=property_info,
            city_info=city_info, uploaded_docs=uploaded_docs
        )
        return property_id
    
    @classmethod
    def update_property(cls, property_documents, payload):
        _payload = copy.deepcopy(payload)
        property_id = _payload.get("property_id")
        if not property_id:
            raise HttpException(error="ProperyId is a required field to update details",
                                status_code=400)

        uploaded_docs = None
        if property_documents:
            uploaded_docs = cls.upload_property_documents_to_s3(property_documents)

        property_id = PropertyListingService.update_property(
            property_id=property_id, uploaded_docs=uploaded_docs, payload=_payload
        )
        return property_id