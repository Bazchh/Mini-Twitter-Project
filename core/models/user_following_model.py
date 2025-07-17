"""
This module defines the UserFollowing model to represent follow relationships between users.
"""
from django.db import models
from core.models.base_model import BaseModel
from core.models.user_model import User


class UserFollowing(BaseModel):
    """
    Model representing a user following another user.
    """
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)

    class Meta:
        """
        Meta class for UserFollowing.
        """
        unique_together = ('followed', 'following')