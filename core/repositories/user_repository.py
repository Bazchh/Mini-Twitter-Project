from django.core.exceptions import ObjectDoesNotExist
from core.models.user_model import User
from core.shared.customAPIException import CustomAPIException
class UserRepository:
    @staticmethod
    def get_all_users():
        try:
            return User.objects.all()
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving users: " + str(e), status_code=500)

    @staticmethod
    def get_user_by_id(user_id):
        try:
            return User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise CustomAPIException(detail='User not found.', status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving user: " + str(e), status_code=500)

    @staticmethod
    def create_user(validated_data):
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except Exception as e:
            raise CustomAPIException(detail="Error creating user: " + str(e), status_code=400)

    @staticmethod
    def update_user(user_id, validated_data):
        try:
            user = User.objects.get(id=user_id)
            new_email = validated_data.get('email')
            if new_email and new_email != user.email:
                if User.objects.filter(email=new_email).exists():
                    raise CustomAPIException(detail="Email existente e em uso",status_code=400)
            for attr, value in validated_data.items():
                setattr(user, attr, value)
            
            if 'password' in validated_data:
                user.set_password(validated_data['password'])
            
            user.save()
            return user
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="User not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error updating user: " + str(e), status_code=400)

    @staticmethod
    def delete_user(user_id):
        try:
            user = UserRepository.get_user_by_id(user_id)
            user.status = 'inactive'
            user.save()
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="User not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error deleting user: " + str(e), status_code=400)
