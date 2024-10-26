from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from core.views.token_viewset import CustomTokenPairView
from core.views.user_viewset import UserViewSet
from core.views.profile_viewset import UserProfileViewSet
from core.views.post_viewset import PostViewSet
from core.views.user_following_viewset import UserFollowingViewSet
from core.views.follow_request_viewset import FollowRequestViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'post', PostViewSet, basename='post')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/token/', CustomTokenPairView.as_view(), name='token_obtain_pair'),
        
    path('likes/<uuid:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('likes/<uuid:pk>/likes/', PostViewSet.as_view({'get': 'get_likes'}), name='post-get-likes'),
    
    path('follow_requests/user_requests', FollowRequestViewSet.as_view({'get': 'list'}), name='user_requests'),
    path('follow_requests/send_request/<uuid:user_id>/', FollowRequestViewSet.as_view({'post': 'create'})),
    path('follow_requests/reject-accept/<uuid:pk>/handle/<str:action>/', FollowRequestViewSet.as_view({'put': 'handle_request'})),
    
    path('followings/following/', UserFollowingViewSet.as_view({'get': 'list_following'}), name='list-following'),
    path('followings/followers/', UserFollowingViewSet.as_view({'get': 'list_followers'}), name='list-followers'),
    path('followings/remove-follower/<uuid:follower_id>/', UserFollowingViewSet.as_view({'delete': 'remove_follower'}), name='remove-follower'),
    path('followings/unfollow/<uuid:followed_id>/', UserFollowingViewSet.as_view({'delete': 'unfollow_user'}), name='unfollow-user'),
    path('followings/non_friends/', UserFollowingViewSet.as_view({'get': 'list_non_friends'}), name='list-non-friends')
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
