from django.core.exceptions import ObjectDoesNotExist
from core.models.user_following_model import UserFollowing
from core.shared.customAPIException import CustomAPIException

class UserFollowingRepository:
    @staticmethod
    def get_followings_for_user(user_id):
        """Retorna todos os usuários que o usuário especificado está seguindo."""
        try:
            return UserFollowing.objects.filter(following=user_id)
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving user followings: " + str(e), status_code=500)

    @staticmethod
    def get_followers_for_user(user_id):
        """Retorna todos os seguidores do usuário especificado."""
        try:
            return UserFollowing.objects.filter(following=user_id)
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving user followers: " + str(e), status_code=500)

    @staticmethod
    def create_user_following(validated_data):
        """Cria um novo relacionamento de seguimento."""
        try:
            user_following = UserFollowing.objects.create(**validated_data)
            return user_following
        except Exception as e:
            raise CustomAPIException(detail="Error creating user following: " + str(e), status_code=400)
