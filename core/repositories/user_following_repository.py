"""
This module defines the UserFollowingRepository for handling user following data operations.
"""
from django.core.exceptions import ObjectDoesNotExist
from core.models.user_following_model import UserFollowing
from core.shared.custom_api_exception import CustomAPIException


class UserFollowingRepository:
    """
    Repository class for managing UserFollowing objects.
    Handles operations related to user followings and followers.
    """

    @staticmethod
    def get_followings_for_user(user_id):
        """
        Retorna todos os usuários que o usuário especificado está seguindo.
        """
        try:
            # 'following' é quem está seguindo, 'followed' é quem é seguido
            # Se quero quem o user_id ESTÁ SEGUINDO, então user_id é o 'following'
            return UserFollowing.objects.filter(following__id=user_id)
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error retrieving user followings: {e}", status_code=500
            ) from e

    @staticmethod
    def get_followers_for_user(user_id):
        """
        Retorna todos os seguidores do usuário especificado.
        """
        try:
            # Se quero os SEGUIDORES do user_id, então user_id é o 'followed'
            return UserFollowing.objects.filter(followed__id=user_id)
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error retrieving user followers: {e}", status_code=500
            ) from e

    @staticmethod
    def create_user_following(validated_data):
        """
        Cria um novo relacionamento de seguimento.
        """
        try:
            user_following = UserFollowing.objects.create(**validated_data)
            return user_following
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error creating user following: {e}", status_code=400
            ) from e
