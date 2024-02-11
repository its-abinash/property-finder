from django.contrib.auth import authenticate, login, logout
from common.custom_exceptions import HttpException
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from authentication.serializers import CurrentUserSerializer

class AuthenticationUtils:

    @classmethod
    def login_user(cls, request, request_details):
        user = None
        username = request_details.get('username')
        password = request_details.get('password')
        contact_number = request_details.get('contact_number')
        if not username and contact_number:
            user = authenticate(contact_number=contact_number, password=password)
        if not user and username and not contact_number:
            user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        if not user:
            raise HttpException(error="Invalid Credentials",
                                status_code=401)
    
    @classmethod
    def register_user(cls, request, request_details):
        username = request_details.get('username')
        email = request_details.get('email')
        password = request_details.get('password')
        contact_number = request_details.get('contact_number')
        full_name = request_details.get('full_name') or ''
        first_name = request_details.get('first_name') or ''
        last_name = request_details.get('last_name') or ''
        last_login = request_details.get("last_login")
        last_login = timezone.now()
        user_model = get_user_model()
        user = user_model.objects.create(
            username=username, contact_number=contact_number, email=email,
            first_name=first_name, last_name=last_name, last_login=last_login,
            is_contact_number_verified=False, password=password,
            is_active=True, full_name=full_name)
        user.set_password(password)
        user.backend = settings.DJANGO_MODEL_BACKEND
        user.save()
        login(request, user)
        if not user:
            raise HttpException(error="Could not register user",
                                status_code=400)
        return user and user.id
    
    @classmethod
    def logout_user(cls, request):
        logout(request)
    
    @classmethod
    def get_user_data(cls, request):
        if request.user.is_authenticated:
            user_data = CurrentUserSerializer(request.user).data
            return user_data
        else:
            raise HttpException(error={"error": "User Unauthenticated"},
                                status_code=status.HTTP_401_UNAUTHORIZED)