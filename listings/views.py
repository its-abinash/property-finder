from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from listings.utils import PropertyListingUtil
from common.utils import return_success_response

class PropertyListingsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        property_id = self.kwargs.get("property_id")
        params = dict(request.query_params)
        data = PropertyListingUtil.get_properties_details(property_id=property_id, **params)
        return return_success_response(data)

    def post(self, request):
        form_data = request.data
        property_documents = request.FILES['property_documents']
        property_id = PropertyListingUtil.add_property_details(form_data, property_documents)
        if property_id:
            return return_success_response({
                "message": "Property created with id: {}".format(property_id)})

    def put(self, request):
        data = request.data
        property_documents = request.FILES.get('property_documents')
        property_id = PropertyListingUtil.update_property(property_documents, data)

        return return_success_response({
            "message": "Property details updated for id: {}".format(property_id)})

class PropertyListingView(PropertyListingsView):
    ...