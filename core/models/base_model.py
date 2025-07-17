"""
This module defines the BaseModel, which provides common fields for other models.
"""
import uuid
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    BaseModel provides common fields like id, created_at, and updated_at.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for BaseModel.
        """
        abstract = True