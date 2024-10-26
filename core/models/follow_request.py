from core.models.base_model import BaseModel
from core.models.user_model import User
from core.models.user_following_model import UserFollowing
from django.db import models
from django.core.exceptions import ValidationError

class FollowRequest(BaseModel):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    FOLLOW_REQUEST_STATUS = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    requester = models.ForeignKey(User, related_name='sent_follow_requests', on_delete=models.CASCADE)
    requested = models.ForeignKey(User, related_name='received_follow_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=FOLLOW_REQUEST_STATUS, default=PENDING)

    class Meta:
        unique_together = ('requester', 'requested')

    def clean(self):
        if UserFollowing.objects.filter(followed=self.requested, following=self.requester).exists():
            raise ValidationError("Você já está seguindo esse usuário.")

    def accept(self):  
     if self.status == self.ACCEPTED:
      raise ValidationError("Asolicitação já foi aceita")
    
     self.status = self.ACCEPTED
     self.save()

     UserFollowing.objects.create(
            followed=self.requested,
            following=self.requester
        )
     
    def reject(self):
        if self.status == self.REJECTED:
            raise ValidationError("A solicitação já foi rejeitada.")
        
        self.status = self.REJECTED
        self.save()