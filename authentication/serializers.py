from rest_framework import serializers
from django.contrib.auth import get_user_model

class CurrentUserSerializer(serializers.ModelSerializer):
    contact_info = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(CurrentUserSerializer, self).__init__(*args, **kwargs)

    def get_contact_info(self, obj):
        data = {
            'contact_number': getattr(obj, 'contact_number', None),
            'email': getattr(obj, 'email', None),
            'first_name': getattr(obj, 'first_name', None),
            'last_name': getattr(obj, 'last_name', None),
            'full_name': getattr(obj, 'full_name', None)
        }
        return data


    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'contact_info')