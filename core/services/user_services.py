from core.repositories.user_repository import UserRepository
from core.shared.customAPIException import CustomAPIException
from core.repositories.profile_repository import UserProfileRepository

class UserService:
    @staticmethod
    def list_all_users():
        try:
            return UserRepository.get_all_users()
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def retrieve_user(user_id):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                raise CustomAPIException(detail='User not found.', status_code=404)
            return user
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def create_user(validated_data):
        try:
            user = UserRepository.create_user(validated_data)
            # Criar o perfil do usuário imediatamente após a criação do usuário
            UserProfileRepository.create_profile({'user': user})
            return user
        except Exception as e:
            raise CustomAPIException(detail="Failed to create user: " + str(e), status_code=400)

    @staticmethod
    def update_user(user_id, validated_data):
        try:
            return UserRepository.update_user(user_id, validated_data)
        except Exception as e:
            raise CustomAPIException(detail="Failed to update user: " + str(e), status_code=400)

    @staticmethod
    def delete_user(user_id):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                raise CustomAPIException(detail="User not found.", status_code=404)
            UserRepository.delete_user(user_id) 
        except Exception as e:
            raise CustomAPIException(detail="Failed to delete user: " + str(e), status_code=400)
