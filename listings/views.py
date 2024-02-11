from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from listings.utils import PropertyListingUtil
from rest_framework import parsers
from listings.interface.database_service import PropertyListingService

class PropertyListingsView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def get(self, request):
        data = PropertyListingUtil.get_properties_details(request.kwargs)
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        form_data = request.data
        property_id = PropertyListingService.create_property(form_data)
        if property_id:
            return Response(data={"message": "Property created with id: {}".format(property_id)},
                            status=status.HTTP_201_CREATED)
        return Response(data={"message": "Error while creating Property"},
                        status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        form_data = request.data
        property_id = PropertyListingService.update_property(form_data)
        
        return Response(data={"message": "Property details updated for id: {}".format(property_id)},
                            status=status.HTTP_201_CREATED)

class PropertyListingView(PropertyListingsView):
    ...