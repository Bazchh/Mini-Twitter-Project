from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from core.models.post_model import Post
from core.models.user_following_model import UserFollowing
from core.serializers.post_serializer import PostSerializer

class FeedPagination(PageNumberPagination):
    page_size = 10 

class FeedViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]  

    def list(self, request):
        user = request.user

        followed_users = UserFollowing.objects.filter(following=user).values_list('followed', flat=True)

        posts = Post.objects.filter(user__id__in=followed_users).order_by('-created_at')

        paginator = FeedPagination()
        paginated_posts = paginator.paginate_queryset(posts, request)
        
        serializer = PostSerializer(paginated_posts, many=True)
        
        return paginator.get_paginated_response(serializer.data)
