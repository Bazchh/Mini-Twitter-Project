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
    path('likes/<uuid:pk>/likes/', PostViewSet.as_view({'get': 'get_likes'}), name='post-get-likes')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
