from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from core.serializers.profile_serializer import UserProfileSerializer
from core.services.profile_service import UserProfileService
from core.shared.customAPIException import CustomAPIException
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from core.repositories.profile_repository import UserProfileRepository


class UserProfilePagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class UserProfileViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    pagination_class = UserProfilePagination
    
    
    def list(self, request):
        try:
            paginator = self.pagination_class()
            profiles = UserProfileService.list_all_profiles()
            page = paginator.paginate_queryset(profiles, request)
            serializer = UserProfileSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def retrieve(self, request, pk=None):
        try:
            profile = UserProfileService.retrieve_profile(pk)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def create(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Associa o perfil ao usuário autenticado
                validated_data = serializer.validated_data
                # Adiciona o usuário autenticado ao dicionário de dados validados
                validated_data['user'] = request.user
                # Cria o perfil com os dados validados, incluindo o usuário
                profile = UserProfileService.create_profile(validated_data)
                response_serializer = UserProfileSerializer(profile)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except CustomAPIException as e:
                return Response({'detail': str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request):
        logged_user = request.user  # O usuário autenticado
        validated_data = request.data  # Dados que serão validados
        profile = UserProfileRepository.update_profile(logged_user, validated_data)
        return Response(UserProfileSerializer(profile).data)


    def destroy(self, request, pk=None):
        try:
            UserProfileService.delete_profile(pk, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)
