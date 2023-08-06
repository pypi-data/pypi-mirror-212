import jwt

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.conf import settings

from djangoauthtoken.models import TokenUser, Token

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def refresh_token(request):
    """
    Refresh Token request.
    """
    try:
        data = request.data
        refresh_token = data['refresh_token']
        refresh_token_decode = jwt.decode(refresh_token,
                                        settings.JWT_SECRET,
                                        algorithms=settings.JWT_ALGO)

        print(refresh_token_decode)

        user = TokenUser.objects.get(id=refresh_token_decode['user_id'])
        user_token = Token.objects.get(user=user, refresh_token=refresh_token)
        token = Token(user=user)
        token.save()
        print(token.id)

        return Response({
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "token": token.token,
                    "refresh_token": token.refresh_token,
                    "expires_at": token.expiry_time
                    },
                    status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

