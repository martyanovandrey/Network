from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def serialize(self):
        return {
            'id': self.id,
            "username": self.username
        }

    pass


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    text = models.CharField(max_length=255)
    likes = models.ManyToManyField('User', blank=True, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.likes}"  

    @property
    def num_like(self):
        return self.likes.all().count()  

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            'text': self.text,
            "likes": self.likes.all().count(),
            'timestamp': self.timestamp.strftime("%b %#d %Y, %#I:%M %p")
        }

class UserFollowing(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    following_user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")

    def serialize(self):
        return {
            'user_id': self.user_id.username,
            "following_user_id": self.following_user_id.username
        }

    class Meta:
        unique_together = ['user_id', 'following_user_id']



        