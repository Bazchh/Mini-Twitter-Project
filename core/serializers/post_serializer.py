from rest_framework import serializers
from core.models.post_model import Post

class PostSerializer(serializers.ModelSerializer):
    image = serializers.FileField()
    
    class Meta:
        model = Post
        fields = ['id','title', 'text', 'image', 'likes', 'created_at', 'updated_at']
        read_only_fields = ['id','likes', 'created_at', 'updated_at']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
