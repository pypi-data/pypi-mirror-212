from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from djangoauthtoken.models import TokenUser

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def sign_up(request):
    """
    Sign up request
    """
    try:
        data = request.data
        username = data['username']
        email = data['email']
        password = data['password']

        user, exists = TokenUser.objects.get_or_create(
            username=username,
            email=email,
            password=password
        )

        if not exists:
            raise Exception
        
        return Response({
            "username": user.username,
            "email": user.email,
            "id": user.id
        }, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

