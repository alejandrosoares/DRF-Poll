from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.views import APIView

from utils.views.response.builder import build_bad_request_response
from utils.authentication import BasicAuthentication
from .models import User
from .serializers import UserListSerializer, UserCreateSerializer
from .utils.views.login import build_login_response
from .utils.constants import BAD_CREDENTIALS


class UserListView(BasicAuthentication, 
                generics.ListAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserCreateView(generics.CreateAPIView):

    serializer_class = UserCreateSerializer


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):

    permission_classes = []
    
    def post(self, request,):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return build_login_response(user)
        return build_bad_request_response(BAD_CREDENTIALS)

