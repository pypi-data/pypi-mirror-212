from rest_framework import serializers
from djangoauthtoken.models import TokenUser as User

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            'password', 
            'last_login',
            'is_superuser',
            'is_staff',
            'is_active',
            'groups',
            'user_permissions'
            ]