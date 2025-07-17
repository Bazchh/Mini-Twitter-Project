"""
This module defines the UserProfileRepository for handling user profile data operations.
"""
from django.core.exceptions import ObjectDoesNotExist
from core.models.profile_model import UserProfile
from core.shared.custom_api_exception import CustomAPIException
from core.models.user_model import User


class UserProfileRepository:
    """
    Repository class for managing UserProfile objects.
    Handles CRUD operations and specific profile retrieval.
    """

    @staticmethod
    def get_all_profiles():
        """
        Retrieves all user profiles.
        Raises CustomAPIException on database error.
        """
        try:
            return UserProfile.objects.all()
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error retrieving profiles: {e}", status_code=500
            ) from e

    @staticmethod
    def get_profile_by_user_id(user_id):
        """
        Retrieves a user profile by the associated user's ID.
        Raises CustomAPIException if the profile is not found or on database error.
        """
        try:
            return UserProfile.objects.get(user_id=user_id)
        except ObjectDoesNotExist as exc:
            raise CustomAPIException(detail='Profile not found.', status_code=404) from exc
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error retrieving profile: {e}", status_code=500
            ) from e

    @staticmethod
    def get_profile_by_id(profile_id):
        """
        Retrieves a user profile by its own ID.
        Raises CustomAPIException if the profile is not found or on database error.
        """
        try:
            return UserProfile.objects.get(id=profile_id)
        except ObjectDoesNotExist as exc:
            raise CustomAPIException(detail="Profile not found.", status_code=404) from exc
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error retrieving profile: {e}", status_code=500
            ) from e

    @staticmethod
    def create_profile(validated_data):
        """
        Creates a new user profile with validated data.
        Assumes 'user' field is included in validated_data.
        Raises CustomAPIException on creation error.
        """
        try:
            # Cria o perfil com os dados validados, que já incluem o campo 'user'
            profile = UserProfile.objects.create(**validated_data)
            return profile
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error creating profile: {e}", status_code=400
            ) from e

    @staticmethod
    def update_profile(logged_user, validated_data):
        """
        Updates the profile of the logged-in user.
        Raises CustomAPIException if the profile is not found or on update error.
        """
        try:
            # Tenta encontrar o perfil do usuário logado
            profile = UserProfile.objects.get(user=logged_user)

            # Atualiza os campos válidos no perfil
            for attr, value in validated_data.items():
                setattr(profile, attr, value)

            # Salva as alterações
            profile.save()
            return profile
        except ObjectDoesNotExist as exc:
            raise CustomAPIException(detail="Profile not found.", status_code=404) from exc
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error updating profile: {e}", status_code=400
            ) from e

    @staticmethod
    def delete_user(logged_user, user_id):
        """
        Deactivates a user account (sets status to 'inactive').
        Requires the logged-in user to be the same as the user to be deactivated.
        Raises CustomAPIException for permission issues, user not found, or other errors.
        """
        if logged_user.id != user_id:
            raise CustomAPIException(
                detail="You do not have permission to delete this user.", status_code=403
            )

        try:
            user = User.objects.get(id=user_id)
            user.status = 'inactive'
            user.save()
            # Retornar True ou o próprio user para indicar sucesso da desativação
            return True
        except ObjectDoesNotExist as exc:
            raise CustomAPIException(detail="User not found.", status_code=404) from exc
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error deleting user: {e}", status_code=400
            ) from e
