from rest_framework import serializers
from core.models.profile_model import UserProfile
from core.models.user_model import User

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  

    class Meta:
        model = UserProfile
        fields = ['user', 'description', 'rating', 'privacy']
