import json
from django.http import HttpResponse
from rest_framework import viewsets

from djangoauthtoken.models import TokenUser
from djangoauthtoken.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = TokenUser.objects.all()
    serializer_class = UserSerializer
