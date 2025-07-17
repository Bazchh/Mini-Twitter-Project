"""
This module defines the UserService for handling user-related business logic.
"""
from core.repositories.user_repository import UserRepository
from core.shared.custom_api_exception import CustomAPIException
from core.repositories.profile_repository import UserProfileRepository
from django.core.exceptions import ObjectDoesNotExist


class UserService:
    """
    Service class for managing User objects and their associated business logic.
    """

    @staticmethod
    def list_all_users():
        """
        Lists all user objects using the UserRepository.
        Raises CustomAPIException on retrieval error.
        """
        try:
            return UserRepository.get_all_users()
        except CustomAPIException as exc:
            # Re-lança CustomAPIException vindas do repositório
            raise exc
        except Exception as e:
            # Captura outras exceções inesperadas
            raise CustomAPIException(detail=f"Error retrieving users: {e}", status_code=500) from e

    @staticmethod
    def retrieve_user(user_id):
        """
        Retrieves a single user object by its ID using the UserRepository.
        Raises CustomAPIException if the user is not found or on retrieval error.
        """
        try:
            user = UserRepository.get_user_by_id(user_id)
            # A verificação 'if not user' pode ser redundante se o repositório já lança ObjectDoesNotExist
            # e isso é traduzido para CustomAPIException pelo repositório.
            # Se o repositório já lança 404, esta linha não é necessária.
            # if not user:
            #    raise CustomAPIException(detail='User not found.', status_code=404)
            return user
        except CustomAPIException as exc:
            # Re-lança CustomAPIException vindas do repositório
            raise exc
        except Exception as e:
            # Captura outras exceções inesperadas
            raise CustomAPIException(detail=f"Error retrieving user: {e}", status_code=500) from e

    @staticmethod
    def create_user(validated_data):
        """
        Creates a new user and automatically creates a corresponding user profile.
        Raises CustomAPIException if user or profile creation fails.
        """
        try:
            user = UserRepository.create_user(validated_data)
            # Criar o perfil do usuário imediatamente após a criação do usuário
            UserProfileRepository.create_profile({'user': user})
            return user
        except CustomAPIException as exc:
            # Re-lança CustomAPIException vindas do repositório
            raise exc
        except Exception as e:
            # Captura outras exceções inesperadas
            raise CustomAPIException(detail=f"Failed to create user: {e}", status_code=400) from e

    @staticmethod
    def update_user(user_id, validated_data):
        """
        Updates an existing user's information using the UserRepository.
        Raises CustomAPIException if user not found or update fails.
        """
        try:
            return UserRepository.update_user(user_id, validated_data)
        except CustomAPIException as exc:
            # Re-lança CustomAPIException vindas do repositório
            raise exc
        except Exception as e:
            # Captura outras exceções inesperadas
            raise CustomAPIException(detail=f"Failed to update user: {e}", status_code=400) from e

    @staticmethod
    def delete_user(user_id):
        """
        Deactivates a user account using the UserRepository.
        Raises CustomAPIException if user not found or deletion/deactivation fails.
        """
        try:
            # UserRepository.delete_user já lida com a busca e desativação
            # e também levanta exceções como CustomAPIException se o usuário não for encontrado.
            UserRepository.delete_user(user_id)
            return {"detail": "User deactivated successfully."} # Retorno para indicar sucesso
        except CustomAPIException as exc:
            # Re-lança CustomAPIException vindas do repositório
            raise exc
        except Exception as e:
            # Captura outras exceções inesperadas
            raise CustomAPIException(detail=f"Failed to delete user: {e}", status_code=400) from e
