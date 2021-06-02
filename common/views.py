from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.parsers import MultiPartParser

from core.models import User
from .serializers import UserSerializer

class RegisterAPIView(APIView):
   
    def post(self, request):
        data = request.data
        
        #Remove immutability
        # if not request.POST._mutable:
        #     request.POST._mutable = True

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException({ 'error': True, 'msg': 'Passwords do not match!'})

        data['is_ambassador'] = 0

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({ 'error': False, 'data': serializer.data})


class LoginAPIView(APIView):
    # handle login
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        print('email', email)
        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed({ "error": True, "msg":'User not found!'})


        if not user.check_password(password):
            raise exceptions.AuthenticationFailed({ "error": True, "msg": "Incorrect Password"})

        serializer = UserSerializer(user)
        return Response({ 'error': False, "msg": "login Successfuly", "user": serializer.data})    
