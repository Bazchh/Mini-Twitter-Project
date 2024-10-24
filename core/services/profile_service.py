from core.repositories.profile_repository import UserProfileRepository
from core.shared.customAPIException import CustomAPIException
from django.core.exceptions import ObjectDoesNotExist
from core.models.profile_model import UserProfile
from rest_framework.exceptions import PermissionDenied
from core.repositories.user_repository import UserRepository

class UserProfileService:
    @staticmethod
    def list_all_profiles():
        try:
            return UserProfileRepository.get_all_profiles()
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def retrieve_profile(user_id):
        try:
            profile = UserProfileRepository.get_profile_by_user_id(user_id)
            if not profile:
                raise CustomAPIException(detail='Profile not found.', status_code=404)
            return profile
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)


    @staticmethod
    def create_profile(validated_data):
        try:
            return UserProfileRepository.create_profile(validated_data)
        except Exception as e:
            raise CustomAPIException(detail="Failed to create profile: " + str(e), status_code=400)

    @staticmethod
    def update_profile(logged_in_user, validated_data):
        try:
            profile = UserProfile.objects.get(user_id=logged_in_user.id)
            
            if profile.user_id != logged_in_user.id:
                raise CustomAPIException(detail="You do not have permission to update this profile.", status_code=403)
            
            for attr, value in validated_data.items():
                setattr(profile, attr, value)
            
            profile.save()
            return profile

        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Profile not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error updating profile: " + str(e), status_code=400)



    @staticmethod
    def delete_profile(user_id, current_user):
        try:
            profile = UserProfileRepository.get_profile_by_user_id(user_id)
            if not profile:
                raise CustomAPIException(detail="Profile not found.", status_code=404)
            
            if profile.user.id != current_user.id:
                raise PermissionDenied("You can only delete your own profile.")
            
            UserRepository.delete_user(user_id) 
        except PermissionDenied as e:
            raise CustomAPIException(detail=str(e), status_code=403)
        except Exception as e:
            raise CustomAPIException(detail="Failed to delete profile: " + str(e), status_code=400)

