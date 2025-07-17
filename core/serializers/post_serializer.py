"""
This module defines the PostSerializer for serializing and validating post data.
"""
from rest_framework import serializers
from core.models.post_model import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    Handles serialization, creation, and updating of post instances.
    """
    image = serializers.FileField(required=False, allow_null=True)

    class Meta:
        """
        Meta class for PostSerializer.
        """
        model = Post
        fields = ['id', 'title', 'text', 'image', 'likes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'likes', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Creates and returns a new `Post` instance, given the validated data.
        """
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Updates and returns an existing `Post` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
