from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    text = models.CharField(max_length=255)
    likes = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.timestamp}"    

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            'text': self.text,
            'likes': self.likes,
            'timestamp': self.timestamp.strftime("%b %#d %Y, %#I:%M %p")
        }