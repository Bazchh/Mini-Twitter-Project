from core.models.follow_request import FollowRequest
from core.shared.customAPIException import CustomAPIException
from core.repositories.follow_request_repository import FollowRequestRepository
from rest_framework import status
from core.services.user_following_service import UserFollowingService
class FollowRequestService:
    @staticmethod
    def list_all_follow_requests_for_user(user_id):
        try:
            return FollowRequestRepository.get_follow_requests_for_user(user_id) 
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def retrieve_follow_request(follow_request_id):
        try:
            return FollowRequest.objects.get(id=follow_request_id)
        except FollowRequest.DoesNotExist:
            raise CustomAPIException(detail="FollowRequest not found.", status_code=404)

    @staticmethod
    def create_follow_request(requester_id, requested_id):
        try:
            follow_request = FollowRequestRepository.create_follow_request(requester_id, requested_id)
            return follow_request
        except CustomAPIException as e:
            raise CustomAPIException(detail=str(e.detail), status_code=e.status_code)

    @staticmethod
    def handle_follow_request(follow_request_id, action_type):
        try:
            # Recupera a solicitação de seguimento com status pendente
            follow_request = FollowRequest.objects.get(id=follow_request_id, status=FollowRequest.PENDING)

            if action_type == 'accept':
                follow_request.status = FollowRequest.ACCEPTED

                # Cria o relacionamento de seguimento
                UserFollowingService.update_following_relationship(
                    requester_id=follow_request.requester.id,
                    requested_id=follow_request.requested.id
                )

                # Após criar o relacionamento, exclui a solicitação
                follow_request.delete()
                return {"detail": "Follow request accepted and deleted."}

            elif action_type == 'reject':
                follow_request.status = FollowRequest.REJECTED
                follow_request.save()

                # Após rejeitar a solicitação, exclui a solicitação
                follow_request.delete()
                return {"detail": "Follow request rejected and deleted."}

            else:
                raise CustomAPIException("Ação inválida", status.HTTP_400_BAD_REQUEST)

        except FollowRequest.DoesNotExist:
            raise CustomAPIException("Solicitação de seguimento não encontrada", status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise CustomAPIException("Erro ao manipular a solicitação: " + str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

