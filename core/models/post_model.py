from .base_model import BaseModel
from django.db import models
from core.models.user_model import User
from django.contrib.postgres.fields import ArrayField

class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    text = models.TextField()  
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True) 

    def __str__(self):
        return self.text[:300]
    
    def add_like(self, user):
        if not self.liked_by.filter(id=user.id).exists():
            self.likes += 1
            self.liked_by.add(user)
            self.save()
        else:
            raise ValueError("User has already liked this post.")