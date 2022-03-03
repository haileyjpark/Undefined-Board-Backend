import jwt
from django.http import JsonResponse
from django.conf import settings
from rest_framework import authentication, permissions
from rest_framework.exceptions import AuthenticationFailed
from users.models import User
from django.utils.translation import gettext_lazy as _


secret_key = getattr(settings, 'SECRET_KEY')
algorithm = getattr(settings, 'ALGORITHM')

class MyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user, True)

class MyAuthentication(authentication.TokenAuthentication):
    keyword = "Bearer"
    check_revoked = False

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            msg = _("Invalid token header. No credentials provided.")
            raise AuthenticationFailed(msg)
        
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            msg = _("Invalid token header. No credentials provided.")
            raise AuthenticationFailed(msg)
        
        if len(auth) == 1:
            msg = _("Invalid token header. No credentials provided.")
            raise AuthenticationFailed(msg)
        if len(auth) > 2:
            msg = _("Invalid token header. Token string should not contain spaces.")
            raise AuthenticationFailed(msg)

        try:
            jwt_token = auth[1].decode()
        except UnicodeError:
            msg = _(
                "Invalid token header. Token string should not contain invalid characters."
            )
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(jwt_token)

    def authenticate_credentials(self, jwt_token):
        try:
            if not jwt_token:
                return JsonResponse({'message' : 'TOKEN_REQUIRED'}, status=401)

            payload      = jwt.decode(jwt_token, secret_key, algorithms=[algorithm])
            user         = User.objects.get(id=payload['user_id'])
            return (user, True)

        # except (ValueError, firebase_auth.InvalidIdTokenError):
        #     msg = _("The Firebase token was invalid.")
        #     raise AuthenticationFailed(msg)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)

    


class AuthorizeProduct(authentication.BaseAuthentication):
    def __init__(self, original_function):
        self.original_function = original_function
    
    def __call__(self, request, *args, **kwargs):   
        token = request.headers.get('Authorization')

        if not token:
            request.user = None
            return self.original_function(self, request, *args, **kwargs)
        
        payload      = jwt.decode(token, secret_key, algorithms=[algorithm])

        user         = User.objects.get(id=payload['user_id'])
        request.user = user

        return self.original_function(self, request, *args, **kwargs)
