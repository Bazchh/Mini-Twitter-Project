from rest_framework import serializers
from core.models.user_model import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'cpf', 'email', 'dateOfBirth', 'status', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data.setdefault('is_active', True)
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
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
