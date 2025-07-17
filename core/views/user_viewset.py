from rest_framework.response import Response
from rest_framework import viewsets, status
from core.serializers.user_serializer import UserSerializer
from core.models.user_model import User
from rest_framework.pagination import LimitOffsetPagination
from core.services.user_services import UserService
from core.shared.custom_api_exception import CustomAPIException


class UserPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer
    pagination_class = UserPagination


    def list(self, request):
        users = UserService.list_all_users()
        paginator = self.pagination_class()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            user = UserService.retrieve_user(pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise CustomAPIException(detail='User not found', status_code=404)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_data = serializer.validated_data
                user = UserService.create_user(user_data)
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            except CustomAPIException as e:
                return Response({"detail": str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_data = serializer.validated_data
                user = UserService.update_user(pk, user_data)
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            except CustomAPIException as e:
                return Response({"detail": str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            UserService.delete_user(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            raise CustomAPIException(detail="User not found", status_code=404)
