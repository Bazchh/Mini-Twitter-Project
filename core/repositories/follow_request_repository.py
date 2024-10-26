from django.core.exceptions import ObjectDoesNotExist
from core.models.follow_request import FollowRequest
from core.shared.customAPIException import CustomAPIException
from core.models.user_model import User
from core.repositories.user_following_repository import UserFollowingRepository
from django.db.models import Q

class FollowRequestRepository():
        @staticmethod
        def create_follow_request(requester_id,requested_id):
            try:
                if requester_id == requested_id:
                    raise CustomAPIException(detail="You cannot follow yourself.", status_code=400)
               
                requester = User.objects.get(id=requester_id)
                requested = User.objects.get(id=requested_id)

            
                if FollowRequest.objects.filter(requester=requester, requested=requested, status=FollowRequest.PENDING).exists():
                    raise CustomAPIException(detail="Follow request already pending.", status_code=400)

                follow_request = FollowRequest.objects.create(
                    requester=requester,
                    requested=requested
                )
                return follow_request
            
            except ObjectDoesNotExist:
                raise CustomAPIException(detail="User not found.", status_code=404)
            except Exception as e:
                raise CustomAPIException(detail="Error creating follow request: " + str(e), status_code=500)
            
        @staticmethod
        def get_follow_requests_for_user(user_id):
            try:
                user = User.objects.get(id=user_id)

                follow_requests = FollowRequest.objects.filter(
                    Q(requester=user) | Q(requested=user)
                )
                return follow_requests
            except ObjectDoesNotExist:
                raise CustomAPIException(detail="User not found.", status_code=404)
            except Exception as e:
                raise CustomAPIException(detail="Error retrieving follow requests: " + str(e), status_code=500)
  