"""
This module defines the UserProfileService for handling user profile-related business logic.
"""
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied
from core.models.profile_model import UserProfile
from core.repositories.profile_repository import UserProfileRepository
from core.repositories.user_repository import UserRepository
from core.shared.custom_api_exception import CustomAPIException


class UserProfileService:
    """
    Service class for managing UserProfile objects and their associated business logic.
    """

    @staticmethod
    def list_all_profiles():
        """
        Lists all user profiles using the UserProfileRepository.
        Raises CustomAPIException on retrieval error.
        """
        try:
            return UserProfileRepository.get_all_profiles()
        except CustomAPIException as exc:
            # Re-lança exceções CustomAPIException vindas do repositório
            raise exc
        except Exception as e:
            # Captura outras exceções inesperadas
            raise CustomAPIException(detail=f"Error retrieving profiles: {e}", status_code=500) from e

    @staticmethod
    def retrieve_profile(user_id):
        """
        Retrieves a user profile by the associated user's ID.
        Raises CustomAPIException if the profile is not found or on retrieval error.
        """
        try:
            profile = UserProfileRepository.get_profile_by_user_id(user_id)
            # A verificação 'if not profile' pode ser redundante se o repositório já lança ObjectDoesNotExist
            # e isso é traduzido para CustomAPIException pelo repositório.
            # Se o repositório já lança 404, esta linha não é necessária.
            # if not profile:
            #     raise CustomAPIException(detail='Profile not found.', status_code=404)
            return profile
        except CustomAPIException as exc:
            # Re-lança exceções CustomAPIException vindas do repositório
            raise exc
        except Exception as e:
            raise CustomAPIException(detail=f"Error retrieving profile: {e}", status_code=500) from e

    @staticmethod
    def create_profile(validated_data):
        """
        Creates a new user profile using the UserProfileRepository.
        Raises CustomAPIException if profile creation fails.
        """
        try:
            return UserProfileRepository.create_profile(validated_data)
        except CustomAPIException as exc:
            # Re-lança exceções CustomAPIException vindas do repositório
            raise exc
        except Exception as e:
            raise CustomAPIException(detail=f"Failed to create profile: {e}", status_code=400) from e

    @staticmethod
    def update_profile(logged_in_user, validated_data):
        """
        Updates the profile of the logged-in user.
        Raises CustomAPIException if profile not found, permission denied, or update fails.
        """
        try:
            # Recomenda-se usar o repositório para buscar o perfil
            # profile = UserProfileRepository.get_profile_by_user_id(logged_in_user.id)
            profile = UserProfile.objects.get(user_id=logged_in_user.id) # Usando direto o ORM

            if str(profile.user_id) != str(logged_in_user.id): # Comparação de IDs como string, se for UUID
                raise CustomAPIException(detail="You do not have permission to update this profile.", status_code=403)

            for attr, value in validated_data.items():
                setattr(profile, attr, value)

            profile.save()
            return profile

        except ObjectDoesNotExist as exc:
            raise CustomAPIException(detail="Profile not found.", status_code=404) from exc
        except CustomAPIException as exc:
            # Propaga exceções CustomAPIException (como a de permissão)
            raise exc
        except Exception as e:
            raise CustomAPIException(detail=f"Error updating profile: {e}", status_code=400) from e

    @staticmethod
    def delete_profile(user_id, current_user):
        """
        Deletes a user's profile and deactivates the associated user account.
        Requires the current user to be the owner of the profile being deleted.
        Raises CustomAPIException if profile/user not found, permission denied, or deletion fails.
        """
        try:
            profile = UserProfileRepository.get_profile_by_user_id(user_id)

            # Verifica se o perfil existe antes de verificar a permissão
            if not profile: # Isso pode ser redundante se o repositório já trata NotFound
                raise CustomAPIException(detail="Profile not found.", status_code=404)

            # Usar str() para comparar IDs UUID, que podem ser objetos UUID e não strings diretas
            if str(profile.user.id) != str(current_user.id):
                raise PermissionDenied("You can only delete your own profile.")

            # Assume que UserRepository.delete_user desativa o usuário
            UserRepository.delete_user(user_id)
            return {"detail": "Profile and associated user deactivated successfully."}
        except ObjectDoesNotExist as exc: # Captura se UserProfileRepository não traduziu
            raise CustomAPIException(detail="Profile not found.", status_code=404) from exc
        except PermissionDenied as exc:
            # Traduz a PermissionDenied do DRF para sua CustomAPIException
            raise CustomAPIException(detail=str(exc), status_code=403) from exc
        except CustomAPIException as exc:
            # Captura CustomAPIExceptions vindas de UserRepository.delete_user, por exemplo
            raise exc
        except Exception as e:
            raise CustomAPIException(detail=f"Failed to delete profile: {e}", status_code=400) from e
