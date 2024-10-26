from rest_framework import viewsets, status
from rest_framework.response import Response
from core.services.follow_request_service import FollowRequestService
from core.serializers.follow_request_serializer import FollowRequestSerializer
from core.shared.customAPIException import CustomAPIException
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication 
from rest_framework.decorators import action
from core.services.user_following_service import UserFollowingService
from core.models.follow_request import FollowRequest

class FollowRequestViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestSerializer
    
    def list(self, request):
        follow_requests = FollowRequestService.list_all_follow_requests_for_user(request.user.id)
        serializer = FollowRequestSerializer(follow_requests, many=True)
        return Response(serializer.data)

    def retrieve(self, pk=None):
        try:
            follow_request = FollowRequestService.retrieve_follow_request(pk)
            serializer = FollowRequestSerializer(follow_request)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)

    def create(self, request, user_id=None):
        requester_id = request.user.id  
        requested_id = user_id  

        try:
            if UserFollowingService.is_following(requester_id, requested_id):
                return Response({"detail": "Você já está seguindo este usuário."}, status=status.HTTP_400_BAD_REQUEST)

            follow_request = FollowRequestService.create_follow_request(
                requester_id=requester_id,
                requested_id=requested_id
            )

            response_data = FollowRequestSerializer(follow_request).data
            response_data['requester'] = follow_request.requester.id
            response_data['requested'] = follow_request.requested.id
            
            return Response(response_data, status=status.HTTP_201_CREATED)

        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)


    @action(detail=True, methods=['patch'], url_path='handle/(?P<action>accept|reject)')
    def handle_request(self, request, pk=None, action=None):
        try:
            follow_request = FollowRequestService.retrieve_follow_request(pk)
            
            if request.user.id != follow_request.requested.id:
                return Response({"detail": "Você não tem permissão para aceitar ou rejeitar esta solicitação."}, status=status.HTTP_403_FORBIDDEN)

            result = FollowRequestService.handle_follow_request(follow_request.id, action) 

            return Response(result, status=status.HTTP_200_OK)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)
