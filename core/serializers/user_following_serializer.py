from rest_framework import serializers
from core.models.user_model import User
from core.models.user_following_model import UserFollowing

class UserFollowingSerializer(serializers.ModelSerializer):
    # Aqui ajustamos para que as referências sejam serializadas corretamente
    followed = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserFollowing
        fields = ['id', 'followed', 'following', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, attrs):
        followed = attrs.get('followed')
        following = attrs.get('following')

        if UserFollowing.objects.filter(followed=followed, following=following).exists():
            raise serializers.ValidationError("Você já segue este usuário.")

        return attrs
