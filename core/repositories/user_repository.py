"""
This module defines the UserRepository for handling user data operations.
"""
from django.core.exceptions import ObjectDoesNotExist
from core.models.user_model import User
from core.shared.custom_api_exception import CustomAPIException


class UserRepository:
    """
    Repository class for managing User objects.
    Handles common CRUD operations for User model.
    """

    @staticmethod
    def get_all_users():
        """
        Retrieves all user objects from the database.
        Raises CustomAPIException on database error.
        """
        try:
            return User.objects.all()
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error retrieving users: {e}", status_code=500
            ) from e

    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieves a single user object by its ID.
        Raises CustomAPIException if the user is not found or on database error.
        """
        try:
            return User.objects.get(id=user_id)
        except ObjectDoesNotExist as exc:
            raise CustomAPIException(detail='User not found.', status_code=404) from exc
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error retrieving user: {e}", status_code=500
            ) from e

    @staticmethod
    def create_user(validated_data):
        """
        Creates a new user using validated data.
        Raises CustomAPIException on creation error.
        """
        try:
            # Assumes validated_data contains fields required by create_user,
            # like email, password, name, cpf, dateOfBirth
            user = User.objects.create_user(**validated_data)
            return user
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error creating user: {e}", status_code=400
            ) from e

    @staticmethod
    def update_user(user_id, validated_data):
        """
        Updates an existing user's information.
        Handles email uniqueness check.
        Raises CustomAPIException if user not found, email already in use, or on other errors.
        """
        try:
            user = User.objects.get(id=user_id)
            new_email = validated_data.get('email')

            # Verifica se o email foi alterado e se o novo email já existe
            if new_email and new_email != user.email:
                if User.objects.filter(email=new_email).exists():
                    raise CustomAPIException(detail="Email existente e em uso.", status_code=400)

            # Atualiza os atributos do usuário com os dados validados
            for attr, value in validated_data.items():
                setattr(user, attr, value)

            # Se a senha estiver nos dados validados, use set_password
            if 'password' in validated_data:
                user.set_password(validated_data['password'])

            user.save()
            return user
        except ObjectDoesNotExist as exc:
            raise CustomAPIException(detail="User not found.", status_code=404) from exc
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error updating user: {e}", status_code=400
            ) from e

    @staticmethod
    def delete_user(user_id):
        """
        Deactivates a user account by setting their status to 'inactive'.
        Raises CustomAPIException if user not found or on other errors.
        """
        try:
            user = User.objects.get(id=user_id) # Usar .get() diretamente ou chamar self.get_user_by_id
            user.status = 'inactive'
            user.save()
            return True # Retorna True para indicar que a desativação foi bem-sucedida
        except ObjectDoesNotExist as exc:
            raise CustomAPIException(detail="User not found.", status_code=404) from exc
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error deleting user: {e}", status_code=400
            ) from e
