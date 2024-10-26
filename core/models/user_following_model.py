from core.models.base_model import BaseModel
from core.models.user_model import User
from django.db import models

class UserFollowing(BaseModel):
    followed = models.ForeignKey(User,related_name='followers',on_delete=models.CASCADE)
    following = models.ForeignKey(User,related_name='following', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('followed', 'following')