"""
This module defines the Post model for user-generated posts.
"""
from django.db import models
from core.models.base_model import BaseModel
from core.models.user_model import User
# from django.contrib.postgres.fields import ArrayField # Not used, hence commented out


class Post(BaseModel):
    """
    Represents a user's post with text, image, likes, and liked-by users.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        """
        Returns a string representation of the post, truncated to 300 characters.
        """
        return self.text[:300]

    def add_like(self, user):
        """
        Adds a like to the post from a specific user.
        Raises ValueError if the user has already liked the post.
        """
        if not self.liked_by.filter(id=user.id).exists():
            self.likes += 1
            self.liked_by.add(user)
            self.save()
        else:
            raise ValueError("User has already liked this post.")