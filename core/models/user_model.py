"""
This module defines the custom User model for the application.
"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from core.models.managers import CustomUserManager
from core.models.base_model import BaseModel
from core.validators.user_validator import (
    cpf_regex_validator,
    cpf_min_length_validator,
    validate_email_format,
    name_min_length_validator
)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom User model with additional fields like name, CPF, email, and date of birth.
    """
    name = models.CharField(null=False, blank=False, max_length=100,
    validators=[name_min_length_validator])
    cpf = models.CharField(null=False, blank=False, max_length=11,
      validators=[cpf_regex_validator, cpf_min_length_validator])
    email = models.EmailField(unique=True, validators=[validate_email_format])
    dateOfBirth = models.DateField(null=False, blank=False)
    status = models.CharField(max_length=10, choices=[('active', 'Active'),
    ('inactive', 'Inactive')], default='active')
    is_active = models.BooleanField(default=True)

    # Define que o campo 'email' será utilizado como username (campo único de login)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'cpf', 'dateOfBirth']

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_user_permissions_set',
        blank=True
    )

    class Meta:
        """
        Meta class for User model.
        """
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        """
        Returns the name of the user as its string representation.
        """
        return self.name
