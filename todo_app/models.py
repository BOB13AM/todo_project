from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def serialize(self):
        return {
            "username": self.username,
            "email":self.email,
            "userid":self.id
        }


class task(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="tasks")
    body = models.TextField()
    translated = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True) 

    def serialize(self):
        return {
            "id":self.id,
            "user": self.user.username,
            "body": self.body,
            "translated": self.translated,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }