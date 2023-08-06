from datetime import datetime

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from djangoauthtoken.models import Token

class CustomTokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """
    keyword = 'Bearer'

    def authenticate(self, request):
        
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)
    
    def authenticate_credentials(self, key):
        try:
            # Check for token.
            token = Token.objects.select_related('user').get(token=key)

            # check for expiry time.
            now = datetime.utcnow()
            _diff = now - token.created_at.replace(tzinfo=None)
            if _diff.total_seconds() > token.expiry_time:
                msg = 'Token expired.'
                raise exceptions.AuthenticationFailed(msg)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        return (token.user, token)
    
    def authenticate_header(self, request):
        return self.keyword
