import jwt
import datetime

from rest_framework import authentication, exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import get_authorization_header

from app import settings
from core.models import User


class JWTAuth(BaseAuthentication):

    def authenticate(self, request):
        is_ambassador = 'api/ambassador' in request.path
        #Check User Authentication

        #  token = request.COOKIES.get('jwt')

        # if not token:
        #     return None
        
        auth_data = authentication.get_authorization_header(request)
        print('auth_data', auth_data)

        if not auth_data:
            return None

        prefix, token = auth_data.decode('utf-8').split(' ')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed({
                'error': True, 'msg': 'Your token is invalid'})

    
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed({ 'error': True, 'msg': 'Your token is expired'})



        if (is_ambassador and payload['scope'] != 'ambassador') or (not is_ambassador and payload['scope'] != 'admin'):
             raise exceptions.AuthenticationFailed({
                'error': True, 'msg': 'Invalid Scope'})

        user = User.objects.get(pk=payload['user_id'])

        if user is None:
            raise exceptions.AuthenticationFailed({ 'error': True, 'msg': 'User not found!'})

        return (user, None)

    # Crete JWT
    def generate_jwt(self, id, email, scope):
        payload = {
            'user_id': id,
            'email': email,
            'scope': scope,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow()
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
