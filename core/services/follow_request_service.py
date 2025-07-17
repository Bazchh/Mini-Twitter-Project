"""
This module defines services for handling follow requests.
"""
from core.models.follow_request import FollowRequest
from core.shared.custom_api_exception import CustomAPIException
from core.repositories.follow_request_repository import FollowRequestRepository
from rest_framework import status
from core.services.user_following_service import UserFollowingService


class FollowRequestService:
    """
    Service class for managing follow request business logic.
    """

    @staticmethod
    def list_all_follow_requests_for_user(user_id):
        """
        Lists all follow requests (sent and received) for a specific user.
        Raises CustomAPIException on error.
        """
        try:
            return FollowRequestRepository.get_follow_requests_for_user(user_id)
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500) from e

    @staticmethod
    def retrieve_follow_request(follow_request_id):
        """
        Retrieves a single follow request by its ID.
        Raises CustomAPIException if the request is not found.
        """
        try:
            return FollowRequest.objects.get(id=follow_request_id)
        except FollowRequest.DoesNotExist as exc:
            raise CustomAPIException(detail="FollowRequest not found.", status_code=404) from exc

    @staticmethod
    def create_follow_request(requester_id, requested_id):
        """
        Creates a new follow request.
        Raises CustomAPIException if the request cannot be created (e.g., already pending, self-follow).
        """
        try:
            follow_request = FollowRequestRepository.create_follow_request(requester_id, requested_id)
            return follow_request
        except CustomAPIException as e:
            # Re-lança a CustomAPIException com os detalhes e status code originais
            raise CustomAPIException(detail=str(e.detail), status_code=e.status_code) from e

    @staticmethod
    def handle_follow_request(follow_request_id, action_type):
        """
        Handles accepting or rejecting a pending follow request.
        Accepting creates a following relationship and deletes the request.
        Rejecting deletes the request.
        Raises CustomAPIException for invalid actions or if the request is not found.
        """
        try:
            # Recupera a solicitação de seguimento com status pendente
            follow_request = FollowRequest.objects.get(id=follow_request_id, status=FollowRequest.PENDING)

            if action_type == 'accept':
                # follow_request.status = FollowRequest.ACCEPTED # Não é necessário se for deletar
                # Cria o relacionamento de seguimento através do serviço de user_following
                UserFollowingService.create_following_relationship(
                    follower_id=follow_request.requester.id,
                    followed_id=follow_request.requested.id
                )
                # Após criar o relacionamento, exclui a solicitação pendente
                follow_request.delete()
                return {"detail": "Follow request accepted and deleted."}

            elif action_type == 'reject':
                # follow_request.status = FollowRequest.REJECTED # Não é necessário se for deletar
                # Após rejeitar a solicitação, exclui a solicitação pendente
                follow_request.delete()
                return {"detail": "Follow request rejected and deleted."}

            else:
                raise CustomAPIException("Ação inválida.", status.HTTP_400_BAD_REQUEST)

        except FollowRequest.DoesNotExist as exc:
            raise CustomAPIException("Solicitação de seguimento não encontrada ou não pendente.",
                                     status.HTTP_404_NOT_FOUND) from exc
        except CustomAPIException as exc:
            # Captura CustomAPIExceptions lançadas por UserFollowingService, por exemplo
            raise exc
        except Exception as e:
            raise CustomAPIException(f"Erro ao manipular a solicitação: {e}",
                                     status.HTTP_500_INTERNAL_SERVER_ERROR) from e
