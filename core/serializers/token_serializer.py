"""
This module defines a custom JWT serializer for token generation.
"""
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining JWT token pairs.
    Adds user ID, name, email, and status to the token payload.
    """
    @classmethod
    def get_token(cls, user):
        """
        Generates a token for the given user, adding custom claims.
        """
        token = super().get_token(user)
        token['id'] = str(user.id)
        token['name'] = user.name
        token['email'] = user.email
        token['status'] = 'active' if user.is_active else 'inactive'
        return token
