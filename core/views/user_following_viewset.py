from rest_framework import viewsets, status
from rest_framework.response import Response
from core.services.user_following_service import UserFollowingService
from core.serializers.user_following_serializer import UserFollowingSerializer
from core.shared.custom_api_exception import CustomAPIException
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication 
from core.serializers.user_serializer import UserSerializer
from core.models.user_following_model import UserFollowing
from rest_framework.pagination import LimitOffsetPagination


class UserFollowingPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class UserFollowingViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserFollowing.objects.all()
    serializer_class = UserFollowingSerializer
    pagination_class = UserFollowingPagination

    @action(detail=False, methods=['get'], url_path='following', name='list-following')
    def list_following(self, request):
        try:
            paginator = self.pagination_class()
            user_followings = UserFollowingService.list_followings_for_user(request.user.id)
            page = paginator.paginate_queryset(user_followings, request)
            serializer = UserFollowingSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)

    @action(detail=False, methods=['get'], url_path='followers', name='list-followers')
    def list_followers(self, request):
        paginator = self.pagination_class()
        user_followers = UserFollowingService.list_followers_for_user(request.user.id)
        page = paginator.paginate_queryset(user_followers, request)
        serializer = UserFollowingSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='non_friends', name='list-non-friends')
    def list_non_friends(self, request):
        non_friends = UserFollowingService.list_non_friends(request.user.id)
        serializer = UserSerializer(non_friends, many=True)
        non_friends_data = [{"id": user['id'], "name": user['name']} for user in serializer.data]
        return Response(non_friends_data)

    @action(detail=False, methods=['delete'], url_path='remove_follower/(?P<follower_id>[^/.]+)', name='remove-follower')
    def remove_follower(self, request, follower_id=None):
        try:
            response = UserFollowingService.remove_follower(request.user.id, follower_id)
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)

    @action(detail=False, methods=['delete'], url_path='unfollow/(?P<followed_id>[^/.]+)', name='unfollow-user')
    def unfollow_user(self, request, followed_id=None):
        try:
            UserFollowingService.unfollow_user(request.user.id, followed_id)
            return Response({"detail": "Unfollowed successfully"}, status=status.HTTP_204_NO_CONTENT)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)
