"""
This module defines the UserProfile model.
"""
from django.db import models
from core.models.base_model import BaseModel
from core.models.user_model import User


class UserProfile(BaseModel):
    """
    Model representing a user's profile with additional information.
    """
    PRIVACY_CHOICES = [
        ('public', 'Público'),
        ('private', 'Privado'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    privacy = models.CharField(max_length=7, choices=PRIVACY_CHOICES, default='public')

    class Meta:
        """
        Meta class for UserProfile.
        """
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfiles"

    def __str__(self):
        """
        Returns a string representation of the user profile.
        """
        return f'Perfil de {self.user.name}' # Changed from self.user.username to self.user.name