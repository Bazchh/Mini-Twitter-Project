"""
This module defines the FollowRequestSerializer for serializing and validating follow requests.
"""
from rest_framework import serializers
from core.models.user_model import User
from core.models.follow_request import FollowRequest


class FollowRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the FollowRequest model.
    Handles validation for creating and managing follow requests.
    """
    requester = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    requested = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        """
        Meta class for FollowRequestSerializer.
        """
        model = FollowRequest
        fields = ['id', 'requester', 'requested', 'status', 'created_at', 'updated_at']
        read_only_fields = ['status', 'created_at', 'updated_at']

    def validate(self, attrs):
        """
        Custom validation for FollowRequest creation.
        Ensures a user cannot follow themselves and prevents duplicate pending requests.
        """
        requester = attrs.get('requester')
        requested = attrs.get('requested')

        if requester == requested:
            raise serializers.ValidationError("Você não pode seguir a si mesmo.")

        if FollowRequest.objects.filter(
            requester=requester, requested=requested, status=FollowRequest.PENDING
        ).exists():
            raise serializers.ValidationError("Já existe uma solicitação de seguimento pendente.")

        return attrs
