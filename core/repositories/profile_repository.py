from django.core.exceptions import ObjectDoesNotExist
from core.models.profile_model import UserProfile
from core.shared.customAPIException import CustomAPIException
from core.repositories.user_repository import UserRepository
class UserProfileRepository:
    @staticmethod
    def get_all_profiles():
        try:
            return UserProfile.objects.all()
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving profiles: " + str(e), status_code=500)

    @staticmethod
    def get_profile_by_user_id(user_id):
        try:
            return UserProfile.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            raise CustomAPIException(detail='Profile not found.', status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving profile: " + str(e), status_code=500)
        
    @staticmethod
    def get_profile_by_id(profile_id):
        try:
            return UserProfile.objects.get(id=profile_id)
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Profile not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving profile: " + str(e), status_code=500)


    @staticmethod
    def create_profile(validated_data):
        try:
            # Cria o perfil com os dados validados, que já incluem o campo 'user'
            profile = UserProfile.objects.create(**validated_data)
            return profile
        except Exception as e:
            raise CustomAPIException(detail="Error creating profile: " + str(e), status_code=400)



    @staticmethod
    def update_profile(logged_user, validated_data):
        try:
            # Tenta encontrar o perfil do usuário logado
            profile = UserProfile.objects.get(user=logged_user)

            # Atualiza os campos válidos no perfil
            for attr, value in validated_data.items():
                setattr(profile, attr, value)

            # Salva as alterações
            profile.save()
            return profile
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Profile not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error updating profile: " + str(e), status_code=400)

    @staticmethod
    def delete_user(logged_user, user_id):
        if logged_user.id != user_id:
            raise CustomAPIException(detail="You do not have permission to delete this user.", status_code=403)
        
        try:
            user = UserRepository.get_user_by_id(user_id)
            user.status = 'inactive'  # Marca o usuário como inativo
            user.save()
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="User not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error deleting user: " + str(e), status_code=400)

