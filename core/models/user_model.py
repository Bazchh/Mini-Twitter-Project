from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from core.models.managers import CustomUserManager
from .base_model import BaseModel

from core.validators.user_validator import (
    cpf_regex_validator, 
    cpf_min_length_validator, 
    validate_email_format,
    name_min_length_validator
)

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    name = models.CharField(null=False, blank=False, max_length=100, validators=[name_min_length_validator])
    cpf = models.CharField(null=False, blank=False, max_length=11, validators=[cpf_regex_validator, cpf_min_length_validator])
    email = models.EmailField(unique=True, validators=[validate_email_format])
    dateOfBirth = models.DateField(null=False, blank=False)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    is_active = models.BooleanField(default=True)

    # Define que o campo 'email' será utilizado como username (campo único de login)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'cpf', 'dateOfBirth']
    
    # Custom manager (gerenciador personalizado) para lidar com a criação de usuários e superusuários
    objects = CustomUserManager()

    # Relacionamentos ManyToMany para grupos e permissões, com 'related_name' únicos para evitar conflitos
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
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.name
