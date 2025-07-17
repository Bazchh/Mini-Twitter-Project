"""
This module defines the UserProfileSerializer for serializing and validating user profile data.
"""
from rest_framework import serializers
from core.models.profile_model import UserProfile
from core.models.user_model import User


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    Handles serialization and validation of user profiles.
    """
    # Usamos PrimaryKeyRelatedField para vincular o perfil a um usuário existente.
    # O queryset é necessário para que o DRF saiba quais usuários são válidos.
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        """
        Meta class for UserProfileSerializer.
        """
        model = UserProfile
        fields = ['user', 'description', 'rating', 'privacy']
        read_only_fields = ['rating'] 

