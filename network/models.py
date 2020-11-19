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
    likes = models.ManyToManyField('User', default=None, blank=True, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.timestamp}"  

    @property
    def num_like(self):
        return self.likes.all().count()  

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            'text': self.text,
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

class Like(models.Model):
    post_like = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_like")
    user_like = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_like")

    def serialize(self):
        return {
            'post_like': self.post_like.id,
            "user_like": self.user_like.username
        }

    def __str__(self):
        return str(self.post_like)


        