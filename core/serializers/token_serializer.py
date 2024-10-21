from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = str(user.id)    
        token['name'] = user.name    
        token['email'] = user.email    
        token['status'] = 'active' if user.is_active else 'inactive'
        return token