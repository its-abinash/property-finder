from rest_framework import serializers
from listings.models import Property

class PropertyListingSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(PropertyListingSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Property
        fields = '__all__'