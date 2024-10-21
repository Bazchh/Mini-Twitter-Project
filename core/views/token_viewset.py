from rest_framework_simplejwt.views import TokenObtainPairView
from core.serializers.token_serializer import CustomTokenPairSerializer
from rest_framework.response import Response
from rest_framework import status

class CustomTokenPairView(TokenObtainPairView):
    serializer_class = CustomTokenPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        token = serializer.validated_data['access']
        refresh_token = serializer.validated_data['refresh']

        response_data = {
            'id': str(user.id),
            'name': user.name,
            'email': user.email,
            'status': 'active' if user.is_active else 'inactive',
            'university': user.university.name if hasattr(user, 'university') and user.university else None,
            'access': str(token),
            'refresh': str(refresh_token),
        }

        return Response(response_data, status=status.HTTP_200_OK)