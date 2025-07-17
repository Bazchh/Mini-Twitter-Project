"""
This module defines the UserSerializer for serializing and validating user data.
"""
from rest_framework import serializers
from core.models.user_model import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Handles serialization, creation, and updating of user instances,
    including password handling.
    """
    class Meta:
        """
        Meta class for UserSerializer.
        """
        model = User
        fields = ['id', 'name', 'cpf', 'email', 'dateOfBirth', 'status', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Creates and returns a new `User` instance, given the validated data.
        Sets 'is_active' to True by default.
        """
        validated_data.setdefault('is_active', True)
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Updates and returns an existing `User` instance, given the validated data.
        Handles password hashing if a new password is provided.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.cpf = validated_data.get('cpf', instance.cpf)
        instance.email = validated_data.get('email', instance.email)
        instance.dateOfBirth = validated_data.get('dateOfBirth', instance.dateOfBirth)
        instance.status = validated_data.get('status', instance.status)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance
