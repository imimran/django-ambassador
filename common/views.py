from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework import exceptions, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from core.models import User
from .serializers import UserSerializer
from common.auth import JWTAuth

class RegisterAPIView(APIView):
   
    def post(self, request):
        data = request.data
        
        #Remove immutability
        # if not request.POST._mutable:
        #     request.POST._mutable = True

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException({ 'error': True, 'msg': 'Passwords do not match!'})

        data["is_ambassador"] =  'api/ambassador' in request.path
        print("request.path", request.path)
        #'api/amassador' in request.path

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({ 'error': False, 'data': serializer.data, 'status': status.HTTP_201_CREATED,})


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
        jwt_auth = JWTAuth()

        scope = 'ambassador' if 'api/ambassador' in request.path else 'admin'

        if user.is_ambassador and scope == 'admin':
            raise exceptions.AuthenticationFailed({ "error": True, "msg": "You have no Permission"})

        token = jwt_auth.generate_jwt(user.id, user.email, scope)

        # Set Token in cookies
        # response = Response()
        # response.set_cookie(key='jwt', value=token, httponly=True)
        # response.data = {
        #     'message': 'success'
        # }

        # return response

        return Response({ 'error': False, "msg": "login Successfuly", "user": serializer.data, "token": token})    



# class LogoutAPIView(APIView):
#     """Backend logout"""
#     authentication_classes = [JWTAuth]
#     permission_classes = [IsAuthenticated]

#     def post(self, _):
#         response = Response()
#         response.delete_cookie(key='jwt')
#         response.data = {
#             'message': 'success'
#         }
#         return response


class UserAPIView(APIView):

    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuth]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({ 'error': False, 'user': serializer.data })


class ProfileInfoAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuth]

    def put(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'error': False, 'user': serializer.data})


class ProfilePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuth]

    def put(self, request, pk=None):
        user = request.user
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException({ 'error': True, 'msg': 'Passwords do not match!'})

        user.set_password(data['password'])
        user.save()
        serializer = UserSerializer(user)

        return Response({ 'error': False, 'data': serializer.data })    
