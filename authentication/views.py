from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

class LoginUserView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        ...

class RegisterUserView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        ...

class LogoutUserView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        ...

class CurrentUserView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        ...