from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from authentication.serializers import CurrentUserSerializer
from common.utils import return_success_response
from authentication.utils import AuthenticationUtils

class LoginUserView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        AuthenticationUtils.login_user(request, dict(request.data))
        return return_success_response({'message': 'Login successful'})

class RegisterUserView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user_id = AuthenticationUtils.register_user(request, dict(request.data))
        return return_success_response({"message": "success", "user_id": user_id})

class LogoutUserView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        AuthenticationUtils.logout_user(request)
        return return_success_response({'message': 'Logout successful'})

class CurrentUserView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CurrentUserSerializer

    def get(self, request):
        user_data = AuthenticationUtils.get_user_data(request)
        return return_success_response(user_data)