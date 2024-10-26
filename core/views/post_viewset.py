from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.services.post_service import PostService
from core.serializers.post_serializer import PostSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from drf_spectacular.utils import extend_schema
from core.models.post_model import Post
from core.shared.customAPIException import CustomAPIException
from rest_framework.pagination import PageNumberPagination 

class PostPagination(PageNumberPagination):
    page_size = 10  

class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    
    @extend_schema(
        request=PostSerializer,
        responses={201: PostSerializer},
        description="Create a new post with an optional image.",
    )
    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            try:
                post = PostService.create_post(
                    user=request.user,
                    title=serializer.validated_data['title'],
                    text=serializer.validated_data['text'],
                    image=request.FILES.get('image')
                )
                return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            post = PostService.retrieve_post(pk)
            return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=PostSerializer,
        responses={200: PostSerializer, 400: 'Invalid data', 404: 'Post not found'},
        description="Update an existing post. All fields are optional, but title and text are required."
    )
    def update(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk) 
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PostSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                post = PostService.update_post(
                    post_id=pk,
                    user_id=request.user.id, 
                    title=serializer.validated_data.get('title', post.title),
                    text=serializer.validated_data.get('text', post.text),
                    image=request.FILES.get('image') if 'image' in request.FILES else post.image
                )
                return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
            except CustomAPIException as e:
                return Response({"detail": str(e)}, status=e.status_code)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            PostService.delete_post(user_id=request.user.id, post_id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def like(self, request, pk=None):
        try:
            likes_count = PostService.like_post(post_id=pk, user_id=request.user.id)
            return Response({"likes": likes_count}, status=status.HTTP_200_OK)
        except CustomAPIException as e:
            return Response({"detail": e.detail}, status=e.status_code)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_likes(self, request, pk=None):
        try:
            likes_count = PostService.get_post_likes(post_id=pk)
            return Response({"likes": likes_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        posts = Post.objects.all().order_by('-created_at')  
        paginator = PostPagination()

        paginated_posts = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(paginated_posts, many=True)
        
        return paginator.get_paginated_response(serializer.data)
