"""
This module defines the UserFollowingSerializer for serializing 
and validating user following relationships.
"""
from rest_framework import serializers
from core.models.user_model import User
from core.models.user_following_model import UserFollowing


class UserFollowingSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserFollowing model.
    Handles serialization and validation of follow relationships between users.
    """
    # Aqui ajustamos para que as referências sejam serializadas corretamente
    followed = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        """
        Meta class for UserFollowingSerializer.
        """
        model = UserFollowing
        fields = ['id', 'followed', 'following', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, attrs):
        """
        Custom validation for UserFollowing creation.
        Ensures a duplicate follow relationship does not already exist.
        """
        followed = attrs.get('followed')
        following = attrs.get('following')

        # Verifica se a combinação 'followed' e 'following' já existe
        if UserFollowing.objects.filter(followed=followed, following=following).exists():
            raise serializers.ValidationError("Você já segue este usuário.")

        return attrs
