from .base_model import BaseModel
from django.db import models
from core.models.user_model import User
class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    text = models.TextField()  
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    likes = models.IntegerField(default=0)
    def __str__(self):
        return self.text[:300]
    
    def add_like(self):
        self.likes += 1
        self.save()