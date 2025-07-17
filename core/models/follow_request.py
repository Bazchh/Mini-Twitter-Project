"""
This module defines the FollowRequest model for managing follow requests between users.
"""
from django.db import models
from django.core.exceptions import ValidationError
from core.models.base_model import BaseModel
from core.models.user_model import User
from core.models.user_following_model import UserFollowing


class FollowRequest(BaseModel):
    """
    Model to represent a follow request between two users.
    """
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    FOLLOW_REQUEST_STATUS = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    requester = models.ForeignKey(User, related_name='sent_follow_requests',
                                  on_delete=models.CASCADE)
    requested = models.ForeignKey(User, related_name='received_follow_requests',
                                  on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=FOLLOW_REQUEST_STATUS, default=PENDING)

    class Meta:
        """
        Meta class for FollowRequest.
        """
        unique_together = ('requester', 'requested')

    def clean(self):
        """
        Custom validation to ensure a user isn't already following the requested user.
        """
        if UserFollowing.objects.filter(followed=self.requested, following=self.requester).exists():
            raise ValidationError("Você já está seguindo esse usuário.")

    def accept(self):
        """
        Accepts the follow request and creates a UserFollowing instance.
        """
        if self.status == self.ACCEPTED:
            raise ValidationError("A solicitação já foi aceita.")

        self.status = self.ACCEPTED
        self.save()

        UserFollowing.objects.create(
            followed=self.requested,
            following=self.requester
        )

    def reject(self):
        """
        Rejects the follow request.
        """
        if self.status == self.REJECTED:
            raise ValidationError("A solicitação já foi rejeitada.")

        self.status = self.REJECTED
        self.save()
